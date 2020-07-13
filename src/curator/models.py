from datetime import datetime

from django.db import models
from django.utils.timezone import now

from omens.models import Segment, Translation


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


class SenseTree(models.Model):
    curated_sense = models.TextField(default='')
    ctime = models.DateTimeField(default=now)
    word = models.TextField(default='')
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    curated_by = models.TextField(default='')
    reviewed_by = models.TextField(default='')

    def __str__(self):
        return f'"{self.word}" = {self.curated_sense}'

    def __repr__(self):
        return f'"{self.word}" = {self.curated_sense}'


class Sense(models.Model):
    sense_uri = models.TextField(default='')
    segment = models.ManyToManyField(Segment)

    def __str__(self):
        return self.sense_uri

    def __repr__(self):
        return self.sense_uri
