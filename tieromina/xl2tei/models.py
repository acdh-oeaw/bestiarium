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
        return "{}".format(self.tablet_id)

    

