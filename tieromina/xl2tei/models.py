from django.db import models
from datetime import datetime
from django.utils.timezone import now

from upload.models import Spreadsheet

# Create your models here.
class Tablet(models.Model):
    '''
    Stores the physical tablet information - siglum
    '''
    siglum = models.CharField(max_length=100)
    join = models.CharField(max_length=100, blank=True, null=True)
    ctime = models.DateTimeField (default=now)
    spreadsheet = models.ManyToManyField(Spreadsheet)
    
    def __str__(self):
        return f'{self.siglum}{self.join}'


class Reference(models.Model):
    '''
    Stores references to readings of other authors    
    TODO: Figure out how to store other author information 
          like their names/publication, etc.
    '''
    tablet = models.ForeignKey(Tablet, on_delete=models.CASCADE)
    reflabel = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{str(self.tablet)} - {self.reflabel}'
    

class Chapter(models.Model):
    '''
    Stores the chapter number and 
    links to all the omens 
    that are a part of this chapter
    '''
    chapter_id = models.CharField(max_length=100, primary_key=True)
    ctime = models.DateTimeField (default=now)
    spreadsheet = models.ManyToManyField(Spreadsheet, default='')
    tei = models.TextField(default='')
    tablet = models.ManyToManyField(Tablet)    

    def __str__(self):
        return f'Chapter {self.chapter_id}'


    
class Omen(models.Model):
    '''
    Individual omen
    '''
    omen_id = models.CharField(max_length=100, primary_key=True) # TEI ID
    omen_num = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, default='')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    tablet = models.ManyToManyField(Tablet, blank=True, null=True)        
    reference = models.ManyToManyField(Reference, blank=True, null=True)    

class Token(models.Model):
    '''
    A word/lemma - automatic primary key
    '''
    position = models.IntegerField()
    omen = models.ForeignKey(Omen, on_delete=models.CASCADE)


class Transliteration(models.Model):
    '''
    Transliteration of the token
    '''
    
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default='')

    
class Transcription(models.Model):
    '''
    Transcription
    '''
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default='')
    
    
class Translation(models.Model):
    '''
    Modernlanguage translation (en/de row)
    '''
    lang = models.CharField(max_length=100) # language
    translation_id =  models.CharField(max_length=100, primary_key=True) # TEI ID
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE)    
    text = models.TextField(default='') 

    
class Commentary(models.Model):
    '''
    Philological commentary
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE)    
    text = models.TextField(default='') 

    
class Segment:
    '''
    A segment - either protasis or apodosis
    '''
    token_id = models.CharField(max_length=100, primary_key=True)
    APODOSIS, PROTASIS = 'a', 'p'   
    TYPE_CHOICES = ((APODOSIS, 'apodosis'), (PROTASIS, 'protasis'))

    segment_type = models.CharField(max_length=1,
                                    choices=TYPE_CHOICES,
                                    default=PROTASIS)
    text = models.CharField(max_length=100, blank=True, null=True)
    position = models.IntegerField()
    
