from datetime import datetime

from django.db import models
from django.utils.timezone import now

from omens.models import Chapter


# Create your models here.
class Spreadsheet(models.Model):
    name = models.FileField(blank=False)
    ctime = models.DateTimeField(default=now)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
