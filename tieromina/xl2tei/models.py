from django.db import models
from datetime import datetime
from django.utils.timezone import now

from upload.models import Spreadsheet

# Create your models here.
class Tablet(models.Model):
    '''
    Stores the physical tablet information - siglum
    '''
    tablet_id = models.CharField(max_length=100, primary_key=True)
    ctime = models.DateTimeField (default=now)
    spreadsheet = models.ManyToManyField(Spreadsheet)
    
    def __str__(self):
        return str(self.tablet_id)

    
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

    def __str__(self):
        return f'Chapter {self.chapter_id}'


    
class Omen(models.Model):
    '''
    Individual omen
    '''
    omen_num = models.CharField(max_length=100)
    ctime = models.DateTimeField(default=now)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, default='')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')
    tablet = models.ManyToManyField(Tablet)    

    def __str__(self):
        return f'Omen {self.chapter.chapter_id}.{self.omen_num}'

class Transliteration(models.Model):
    '''
    Transliteration (trl row) 
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')


class Translation(models.Model):
    '''
    Modernlanguage translation (en/de row)
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')



class Transcription(models.Model):
    '''
    Transcription (trs row)
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')


class Commentary(models.Model):
    '''
    Philological commentary
    '''
    omen = models.ForeignKey(Chapter, on_delete=models.CASCADE, default='')

    

    
