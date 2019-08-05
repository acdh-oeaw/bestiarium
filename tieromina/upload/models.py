from django.db import models

# Create your models here.
class Spreadsheet(models.Model):
    name = models.FileField(blank=False)
    ctime = models.DateTimeField

    def __str__(self):
        return "{}".format(self.name)
