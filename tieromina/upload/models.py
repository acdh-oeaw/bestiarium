from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class Spreadsheet(models.Model):
    name = models.FileField(blank=False)
    ctime = models.DateTimeField (default=now)


    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
