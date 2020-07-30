from datetime import datetime

from django.db import models
from django.utils.timezone import now


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
    word_root = models.TextField(default='')
    curated_by = models.TextField(default='')
    reviewed_by = models.TextField(default='')

    def __str__(self):
        return f'"{self.word_root}"'

    def __repr__(self):
        return f'"{self.word_root}" = {self.curated_sense}'


class Sense(models.Model):
    sense_uri = models.TextField(default='')
    sense_tree = models.ForeignKey(SenseTree, on_delete=models.CASCADE)

    def __str__(self):
        return self.sense_uri

    def __repr__(self):
        return self.sense_uri
