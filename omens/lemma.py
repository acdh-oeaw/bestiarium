import logging
import uuid
from xml.etree import ElementTree as ET

from .models import Lemma as LemmaDB
from .namespaces import XML_ID

logger = logging.getLogger(__name__)

APODOSIS_COLOR = "FF00B0F0"


def cell_idx(col_name):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet.index(col_name[-1]) + (len(col_name) - 1) * len(alphabet)


class Token:
    """
    A unit smaller than a chunk - separating breaks/damages from the words and noting where they stop
    """

    def __init__(self, text, fmt, xml_id="", plain_txt=True):
        self.plain_text = plain_txt
        self.text = text
        self.fmt = fmt
        self.xml_id = xml_id

    @property
    def xml_id(self):
        return self._xml_id

    @xml_id.setter
    def xml_id(self, xml_id):
        self._xml_id = xml_id

    def __repr__(self):
        return str(self.__dict__)


class BreakStart(Token):
    """
    Anchor to mark the beginning of a break
    """

    def __init__(self, text, fmt, xml_id):
        super().__init__(text=text, fmt=fmt, xml_id=xml_id, plain_txt=False)
        self.span_to = ""

    @property
    def tei(self):
        if self.text == "[":
            anchor = ET.Element("anchor", {"type": "breakStart"})
            anchor.tail = ""
        elif self.text == "˹":
            anchor = ET.Element("damageSpan", {"spanTo": self.span_to})
            anchor.tail = ""

        return anchor

    @property
    def end_token(self):
        return self._end_token

    @end_token.setter
    def end_token(self, end_token):
        self._end_token = end_token


class BreakEnd(Token):
    """
    Anchor to mark the end of a break
    """

    def __init__(self, text, fmt, xml_id):
        super().__init__(text=text, fmt=fmt, xml_id=xml_id, plain_txt=False)
        self.corresp = ""

    @property
    def tei(self):
        anchor = ET.Element("anchor", {"type": "breakEnd", "corresp": self.corresp})
        anchor.tail = ""
        return anchor


class Missing(Token):
    """
    Missing signs
    """

    def __init__(self, text, fmt):
        super().__init__(text=text, fmt=fmt, plain_txt=False)
        self.quantity = 1

    def widen_gap(self):
        self.quantity += 1

    @property
    def tei(self):

        anchor = ET.Element("gap", {"quantity": self.quantity, "unit": "signs"})
        anchor.tail = ""


class Lemma:
    """
    Lemma as specified in the score
    Equivalent of "Cell"
    """

    def __init__(self, cell, omen):
        self.column_name = cell.column_name
        self.address = cell.address
        self.tokens = []
        token_text = ""
        self.omen = omen
        self.omen_prefix = omen.xml_id
        word_id = ""
        self.apodosis = False
        for chunk in cell.chunks:
            if not chunk.text:
                continue
            if chunk.cell_format.bgcolor == APODOSIS_COLOR:
                self.apodosis = True
            if token_text:
                self.tokens.append(
                    Token(text=token_text, xml_id=word_id, fmt=chunk.cell_format)
                )
                token_text = ""

            word_id = f"{self.omen_prefix}_{cell.address}"
            for pos, char in enumerate(chunk.text):
                anchor_id = f"{self.omen_prefix}_{cell.address}_{pos}"
                if char in "[]˹˺":
                    # TODO: Check that spaces mean nothing in general
                    self.tokens.append(
                        Token(text=token_text, xml_id=anchor_id, fmt=chunk.cell_format)
                    )
                    token_text = ""

                    if char in "[˹":
                        anchor = BreakStart(
                            text=char, xml_id=anchor_id, fmt=chunk.cell_format
                        )
                        self.tokens.append(anchor)
                    elif char in "˺]":
                        random_id = f"{anchor_id}__{uuid.uuid1()}"
                        anchor = BreakEnd(
                            text=char, xml_id=random_id, fmt=chunk.cell_format
                        )
                        self.tokens.append(anchor)
                    elif char == "x":
                        if isinstance(self.tokens[-1], Missing):
                            self.tokens[-1].widen_gap()
                        else:
                            self.tokens.append(Missing(fmt=chunk.cell_format))
                    else:
                        pass
                else:
                    token_text += char

        if token_text:
            self.tokens.append(
                Token(text=token_text, xml_id=word_id, fmt=chunk.cell_format)
            )

        # Add lemma to the model
        # check if lemma exists
        lemma_db = LemmaDB.objects.filter(xml_id__exact=self.xml_id)
        if not lemma_db:
            lemma_db = LemmaDB.objects.create(
                xml_id=self.xml_id,
                omen=omen,
                segment=self.omen.protasis if not self.apodosis else self.omen.apodosis,
                lemma_idx=cell_idx(cell.column_name),
            )

    def __str__(self):
        return f"{self.omen_prefix}_{self.address}"

    def __repr__(self):
        return f"{self.omen_prefix}_{self.address}"

    @property
    def xml_id(self):
        return f"{self.omen_prefix}_w{self.column_name}"

    def score_tei(self, witness, prefix, reference):
        """
        returns the TEI representation
        TODO: Align this with the convention
        """
        fixed_witt = witness.split('______')[0]
        w = ET.Element("rdg", {"wit": fixed_witt})
        if reference:
            w.attrib["source"] = reference

        return self.tei_body(w, prefix)

    def reconstruction_tei(self, prefix):
        w = ET.Element("w", {"corresp": self.xml_id})
        w = self.tei_body(w, prefix)
        return w

    @property
    def plain_text(self):
        return " ".join(t.text for t in self.tokens)

    def tei_body(self, w, prefix):
        w.text = ""
        anchor = None
        for token in self.tokens:
            if token.plain_text is True:
                if anchor is not None:
                    anchor.tail += token.text.replace("<", "").replace(">", "")
                else:
                    w.text += token.text.replace("<", "").replace(">", "")
            else:
                anchor = token.tei

                if "spanTo" in anchor.attrib and not anchor.attrib.get("spanTo", ""):
                    logger.warning(
                        "Empty span to attribute for %s in %s",
                        token,
                        ET.tostring(anchor),
                    )

                anchor.attrib[XML_ID] = token.xml_id
                w.append(anchor)
        return w
