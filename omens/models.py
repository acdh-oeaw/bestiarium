import logging
from xml.etree import ElementTree as ET

from ckeditor.fields import RichTextField

from curator.models import Upload
# Create your models here.
from django.db import models
from django.utils.timezone import now

from .namespaces import NS, TEI_NS, XML_ID, get_attribute
from .util import clean_id, element2string

for ns, uri in NS.items():
    ET.register_namespace(ns, uri)


class Witness(models.Model):
    """
    Stores the physical tablet information - siglum
    Probably unnecessary in the database
    """

    witness_id = models.CharField(max_length=100, primary_key=True)  # siglum
    museum_numbers = models.TextField(blank=True, null=True)
    provenance = models.CharField(max_length=100, blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    state_publication = models.TextField(blank=True, null=True)
    state_preservation = models.TextField(blank=True, null=True)
    manuscript_type = models.TextField(blank=True, null=True)
    tablets_attested = models.TextField(blank=True, null=True)
    omens_attested = models.TextField(blank=True, null=True)
    cdli_number = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    ctime = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.witness_id}: {self.museum_numbers}"

    @property
    def xml_id(self):
        return clean_id(self.witness_id)

    @property
    def tei(self):
        wit = ET.Element(get_attribute("witness", TEI_NS), {XML_ID: self.xml_id})
        idno = ET.SubElement(wit, get_attribute("idno", TEI_NS))
        idno.text = self.witness_id
        return wit

    # @staticmethod
    # def corresponding_witness(cls, witness_label):
    #     """
    #     returns the corresponding witness object (eg. BM 036389+)
    #     given the witness label found in the score (eg. BM 36389+.2)
    #     """
    #     search_str = witness_label.split("+")[0]
    #     return Witness.objects.filter(witness_id__startswith=search_str)


class Chapter(models.Model):
    """
    Stores the chapter number, name and links to omens
    """

    chapter_name = models.CharField(max_length=100, unique=True)
    animal = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    reviewer = models.CharField(max_length=100, blank=True, null=True)
    proofreader = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    ctime = models.DateTimeField(default=now, blank=True, null=True)
    tei = models.TextField(default="", blank=True, null=True)
    witness = models.ManyToManyField(Witness)
    upload = models.ManyToManyField(Upload)
    introduction = RichTextField(default="Page under construction", blank=True, null=True)

    def __str__(self):
        return f"Chapter {self.chapter_name}"

    @property
    def safe_tei(self):
        return self.tei.replace("\n", "").replace("'", "&#8217;")


class Omen(models.Model):
    """
    Individual omen
    """

    xml_id = models.CharField(max_length=100, unique=True)  # TEI ID
    omen_name = models.CharField(max_length=100, primary_key=True)  # TEI @n
    omen_num = models.CharField(max_length=100)  # from sheet name
    ctime = models.DateTimeField(default=now)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default="")
    witness = models.ManyToManyField(Witness)
    upload = models.ManyToManyField(Upload)
    tei_content = models.TextField(blank=True, null=True)

    @property
    def tei(self):
        chapter_tei = ET.XML(self.chapter.tei)
        omen_tei = chapter_tei.find(f'.//*[@n="{self.omen_name}"]')
        if omen_tei:
            return element2string(omen_tei)
        return ""

    @property
    def protasis(self):
        return Segment.objects.filter(xml_id=self.xml_id + "_P")[0]

    @property
    def apodosis(self):
        return Segment.objects.filter(xml_id=self.xml_id + "_A")[0]


class Segment(models.Model):
    """
    A segment in the omen, either PROTASIS or APODOSIS
    """

    xml_id = models.CharField(max_length=100, unique=True)  # TEI ID
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    segment_type = models.CharField(
        max_length=9,
        choices=(("PROTASIS", "Protasis"), ("APODOSIS", "Apodosis")),
        default="PROTASIS",
    )

    @classmethod
    def protasis(cls, omen):
        return cls.objects.filter(xml_id=omen.omen_name + "_P")[0]

    @classmethod
    def apodosis(cls, omen):
        return cls.objects.filter(xml_id=omen.omen_name + "_A")[0]

    def __str__(self):
        return f"Omen {self.omen.omen_name} - {self.segment_type}"


class Lemma(models.Model):
    """
    A lemma in the omen, represented using w element inside the score in the TEI
    """

    xml_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    lemma_idx = models.IntegerField(
        default=0
    )  # index of the lemma in the in the omen (position of the w element, implicit in the TEI)
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)

    def set_segment_type_to_apodosis(self):
        # logging.debug("Changing to Apodosis %s", self.omen.apodosis)
        self.segment = self.omen.apodosis
        self.save()

    def __str__(self):
        return f"{self.xml_id}_{self.segment}"


class Reconstruction(models.Model):
    """
    A reconstruction of the omen, which contains one or more of the following:
    - translation
    - transcription
    - transliteration
    """

    xml_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    label = models.CharField(max_length=100)
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE, default="")
    witness = models.ForeignKey(Witness, on_delete=models.CASCADE, null=True)

    @property
    def safe_id(self):
        return self.xml_id.replace("_", "-").replace(".", "-")


class Translation(models.Model):
    """
    Translation of the omen, corresponding to a particular reconstruction
    """

    xml_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(
        Reconstruction, on_delete=models.CASCADE, default=""
    )
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    translation_txt = models.CharField(max_length=1000, default="")
    lang = models.CharField(
        max_length=2,
        choices=(("en", "ENGLISH"), ("dt", "GERMAN"), ("de", "GERMAN")),
        default="en",
    )

    @property
    def safe_id(self):
        return f"{self.reconstruction.safe_id}-{self.segment.segment_type}"

    def __str__(self):
        return f"{self.xml_id} {self.segment}"


# class Word(models.Model):
#     """
#     Words and word roots from the translation,
#     to be linked with the curated SenseTree later
#     """

#     translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
#     # position of the word in the in the translation segment
#     word_idx = models.IntegerField(default=0)
#     # root form of the word
#     word_root = models.CharField(max_length=100, default="")
#     sense_tree = models.ForeignKey(SenseTree, on_delete=models.CASCADE)


class Transliteration(models.Model):
    """
    A row represents a lemma in a transliteration reconstruction of the omen
    Probably unnecessary
    """

    xml_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(
        Reconstruction, on_delete=models.CASCADE, default=""
    )
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE, default="")


class Transcription(models.Model):
    """
    A row represents a lemma in a transcription of the omen
    Probably unnecessary
    """

    xml_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(
        Reconstruction, on_delete=models.CASCADE, default=""
    )
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE, default="")


class Sequence(models.Model):
    """
    A row represents a named sequence of omens curated
    """

    seq_name = models.CharField(max_length=100, unique=True)
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)


class PhilComment(models.Model):
    """
    A row represents a philological comment
    """

    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.comment:
            return f"{self.comment[:24]}... (Omen: {self.omen.omen_num})"
