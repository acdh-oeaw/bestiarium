from datetime import datetime
from xml.etree import ElementTree as ET

# Create your models here.
from django.db import models
from django.utils.timezone import now

from .namespaces import NS
from .util import element2string

for ns, uri in NS.items():
    ET.register_namespace(ns, uri)


class Witness(models.Model):
    '''
    Stores the physical tablet information - siglum
    '''
    witness_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    siglum = models.CharField(max_length=100)
    joins = models.CharField(max_length=100, blank=True, null=True)
    ctime = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.siglum}+{self.joins}'


class Chapter(models.Model):
    '''
    Stores the chapter number and
    links to all the omens
    that are a part of this chapter
    '''
    chapter_name = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    tei = models.TextField(default='')
    witness = models.ManyToManyField(Witness)

    def __str__(self):
        return f'Chapter {self.chapter_name}'

    @property
    def safe_tei(self):
        return self.tei.replace('\n', '').replace("'", '')


class Omen(models.Model):
    '''
    Individual omen
    '''
    omen_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    omen_num = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    witness = models.ManyToManyField(Witness)

    @property
    def tei(self):
        chapter_tei = ET.XML(self.chapter.tei)
        omen_tei = chapter_tei.find(f'.//*[@n="{self.omen_id}"]')
        return element2string(omen_tei)


class Segment(models.Model):
    '''
    A segment in the omen, either PROTASIS or APODOSIS
    '''
    segment_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    segment_type = models.CharField(max_length=9,
                                    choices=(('PROTASIS', 'Protasis'),
                                             ('APODOSIS', 'Apodosis')),
                                    default='PROTASIS')

    @classmethod
    def protasis(cls, omen):
        print(f"Looking for segment with id: '{omen.omen_id}_P'")
        print("Found ",
              Segment.objects.filter(segment_id=omen.omen_id + '_P')[0])
        return cls.objects.filter(segment_id=omen.omen_id + '_P')[0]

    @classmethod
    def apodosis(cls, omen):
        return cls.objects.filter(segment_id=omen.omen_id + '_A')[0]


class Lemma(models.Model):
    '''
    A lemma in the omen, represented using w element inside the score in the TEI
    '''
    lemma_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    lemma_idx = models.IntegerField(
        default=0
    )  # index of the lemma in the in the omen (position of the w element, implicit in the TEI)
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)

    def set_segment_type_to_apodosis(self):
        print('Changing to Apodosis', self.lemma_id)
        apodosis_segment = Segment.objects.filter(omen=self.omen,
                                                  segment_type='APODOSIS')[0]
        self.segment = apodosis_segment
        self.save()


class Reconstruction(models.Model):
    '''
    A reconstruction of the omen, which contains one or more of the following:
    - translation
    - transcription
    - transliteration
    '''
    reconstruction_id = models.CharField(max_length=100,
                                         primary_key=True)  # TEI ID
    label = models.CharField(max_length=100, default=reconstruction_id)
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE, default='')

    @property
    def safe_id(self):
        return self.reconstruction_id.replace('_', '-').replace('.', '-')


class Translation(models.Model):
    '''
    Translation of the omen, corresponding to a particular reconstruction
    '''
    translation_id = models.CharField(max_length=100,
                                      primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(Reconstruction,
                                       on_delete=models.CASCADE,
                                       default='')
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    translation_txt = models.CharField(max_length=1000, default='')
    lang = models.CharField(max_length=2,
                            choices=(('en', 'ENGLISH'), ('de', 'GERMAN')),
                            default='en')

    @property
    def safe_id(self):
        return f'{self.reconstruction.safe_id}-{self.segment.segment_type}'


class Transliteration(models.Model):
    '''
    A row represents a lemma in a transliteration reconstruction of the omen
    '''
    trl_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(Reconstruction,
                                       on_delete=models.CASCADE,
                                       default='')
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE, default='')


class Transcription(models.Model):
    '''
    A row represents a lemma in a transcription of the omen
    '''
    trs_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(Reconstruction,
                                       on_delete=models.CASCADE,
                                       default='')
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE, default='')
