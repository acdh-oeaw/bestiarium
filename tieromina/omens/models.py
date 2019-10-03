from datetime import datetime

# Create your models here.
from django.db import models
from django.utils.timezone import now


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


class Omen(models.Model):
    '''
    Individual omen
    '''
    omen_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    omen_num = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    witness = models.ManyToManyField(Witness)


class Reconstruction(models.Model):
    '''
    A reconstruction of the omen, which contains one or more of the following:
    - translation
    - transcription
    - transliteration
    '''
    reconstruction_id = models.CharField(
        max_length=100, primary_key=True)  # TEI ID
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE, default='')


class Translation(models.Model):
    '''
    Translation of the omen, corresponding to a particular reconstruction
    '''
    trs_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    reconstruction = models.ForeignKey(
        Reconstruction, on_delete=models.CASCADE, default='')


"""
# Create your models here.
class Tablet(models.Model):
    '''
    Stores the physical tablet information - siglum
    '''
    siglum = models.CharField(max_length=100)
    join = models.CharField(max_length=100, blank=True, null=True)
    ctime = models.DateTimeField(default=now)
    spreadsheet = models.ManyToManyField(Spreadsheet)

    def __str__(self):
        return f'{self.siglum}+{self.join}'


class Reference(models.Model):
    '''
    Stores references to readings of other authors
    TODO: Figure out how to store other author information
          like their names/publication, etc.
    '''
    tablet = models.ForeignKey(Tablet, on_delete=models.CASCADE)
    reflabel = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)

    def __str__(self):
        return f'{str(self.tablet)} - {self.reflabel}'


class Chapter(models.Model):
    '''
    Stores the chapter number and
    links to all the omens
    that are a part of this chapter
    '''
    chapter_id = models.CharField(max_length=100, primary_key=True)
    ctime = models.DateTimeField(default=now)
    spreadsheet = models.ManyToManyField(Spreadsheet, default='')
    tei = models.TextField(default='')
    tablet = models.ManyToManyField(Tablet)

    def __str__(self):
        return f'Chapter {self.chapter_id}'


class Omen(models.Model):
    '''
    Individual omen
    '''
    omen_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    omen_num = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    spreadsheet = models.ForeignKey(
        Spreadsheet, on_delete=models.CASCADE, default='')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    tablet = models.ManyToManyField(Tablet)


APODOSIS, PROTASIS = 'a', 'p'
TYPE_CHOICES = ((APODOSIS, 'apodosis'), (PROTASIS, 'protasis'))


class Token(models.Model):
    '''
    A word/lemma - automatic primary key
    '''
    token_id = models.IntegerField()
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    segment_type = models.CharField(
        max_length=2, choices=TYPE_CHOICES, default=PROTASIS)
    ctime = models.DateTimeField(default=now)


class Reading(models.Model):
    '''
    particular reading of an omen - can be "copy text" or "var" with or without a tablet/reg
    '''
    reading_id = models.CharField(max_length=100, primary_key=True)  # TEI ID
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)
    ctime = models.DateTimeField(default=now)
    reference = models.ForeignKey(
        Reference, on_delete=models.CASCADE, blank=True, null=True)


class Transliteration(models.Model):
    '''
    Transliteration of the token
    '''

    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    reference = models.ForeignKey(
        Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default='')
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    ctime = models.DateTimeField(default=now)


class Transcription(models.Model):
    '''
    Transcription
    '''
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    reference = models.ForeignKey(
        Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default='')
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    ctime = models.DateTimeField(default=now)


class Translation(models.Model):
    '''
    Modernlanguage translation (en/de row)
    '''
    lang = models.CharField(max_length=100)  # language
    translation_id = models.CharField(
        max_length=100, primary_key=True)  # TEI ID
    reference = models.ForeignKey(
        Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default='')
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    ctime = models.DateTimeField(default=now)


class Commentary(models.Model):
    '''
    Philological commentary
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    reference = models.ForeignKey(
        Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default='')
    ctime = models.DateTimeField(default=now)
"""
