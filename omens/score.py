"""
Omen score - gathered from different witnesses
"""
import logging
from collections import UserDict
from typing import List
from xml.etree import ElementTree as ET

from xlsx.cell import Cell

from .lemma import Lemma
from .line import Line
from .namespaces import NS, XML_ID
from .position import Position

logger = logging.getLogger(__name__)


class ScoreLine(Line):
    """
    A line from the score of the omen
    """

    def __init__(self, row: List[Cell], omen, witness):
        super().__init__(omen.xml_id)
        self.omen = omen
        self.reference = ""

        if row[0].column_name == "A":
            idno = row[0].full_text  # noqa: F841
        else:
            logger.error("First cell from column A missing: %s", row)
            raise ValueError(f"col1 must be column A in row: {row}")
        try:
            self.reference = row[1].full_text if row[1].column_name == "B" else ""
        except IndexError:
            pass

        self.witness = witness

        for cell in row:
            if not cell.full_text or cell.column_name in "AB":
                continue

            # determine cell type (position - column/line number or lemma)
            if Position.is_position_cell(cell):  # Position:
                position = Position(cell, self.witness)

                if position.column:
                    self.data.append(position.column)
                self.data.append(position.line)
            else:
                # Lemma
                lemma = Lemma(cell, omen=self.omen)
                self.data.append(lemma)

        self.connect_damaged_ends()


class Score(UserDict):
    """
    A dict of score lines, identified by witness
    """

    def __init__(self, omen):
        super().__init__()
        self.omen = omen
        self.omen_prefix = omen.xml_id

    def add_row(self, row: List[Cell], witness):
        """
        Adds the row to score
        """
        # construct witness
        scoreline = ScoreLine(row, self.omen, witness)
        self.data[scoreline.witness] = scoreline

    @property
    def tei(self):
        """
        returns the TEI representation
        """
        score = ET.Element("div", {"type": "score"})
        ab = ET.SubElement(score, "ab")
        for witness, scoreline in self.data.items():
            for item in scoreline:
                if isinstance(item, Lemma):
                    # construct word identifier
                    # word_id = f'{self.omen_prefix}.{item.xml_id}'
                    word_node = ab.find(f'.//*[@{XML_ID}="{item.xml_id}"]/app', NS)

                    # This is the correct way to check if the node exists
                    # if not Node is True even if find returns a match
                    if word_node is None:
                        # add new /find corresponding word node
                        word_parent = ET.Element("w", {XML_ID: item.xml_id})
                        ab.append(word_parent)
                        word_node = ET.SubElement(word_parent, "app")

                    # Add lemma to the word node
                    word_node.append(
                        item.score_tei(witness, self.omen_prefix, scoreline.reference)
                    )
                else:  # line/column information
                    item_tei = item.tei
                    ab.append(item_tei)

        return score

    @property
    def witnesses(self):
        """
        returns witnesses from the keys
        """
        return list(self.data.keys())
