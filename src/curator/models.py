from datetime import datetime

from django.db import models
from django.utils.timezone import now
from omens.models import Segment


# Create your models here.
class Spreadsheet(models.Model):
    name = models.FileField(blank=False)
    location = models.TextField(default='')
    ctime = models.DateTimeField(default=now)
    user = models.TextField(default='blank')

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class WordSenses(models.Model):
    sense_id = models.TextField(default='')
    ctime = models.DateTimeField(default=now)
    word = models.TextField(default='')
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    curated_by = models.TextField(default='')
    reviewed_by = models.TextField(default='')

    def __str__(self):
        return f'"{self.word}" = {self.sense_id}'

    def __repr__(self):
        return f'"{self.word}" = {self.sense_id}'
