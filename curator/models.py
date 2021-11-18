from django.db import models
from django.utils.timezone import now


class UTYPES:
    INDEX_FILE: str = "index"
    OMEN_FILE: str = "omen"
    DITTO_FILE: str = "ditto"
    COMMENTS_FILE: str = "comments"
    CREDITS_FILE: str = "credits"
    ALL = (INDEX_FILE, OMEN_FILE, DITTO_FILE, COMMENTS_FILE, CREDITS_FILE)


class USTATUS:
    SUCCESS = "success"
    ERROR = "error"


# Create your models here.
class Upload(models.Model):
    name = models.FileField(blank=False)
    location = models.TextField(blank=True)
    ctime = models.DateTimeField(default=now)
    user = models.TextField(blank=False)
    utype = models.TextField(
        blank=False,
        default=UTYPES.OMEN_FILE,
    )
    ustatus = models.TextField(
        blank=False,
        default=USTATUS.SUCCESS,
    )
    report = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class SenseTree(models.Model):
    curated_sense = models.TextField(default="")
    ctime = models.DateTimeField(default=now)
    word_root = models.TextField(default="")
    curated_by = models.TextField(default="")
    reviewed_by = models.TextField(default="")

    def __str__(self):
        return f'"{self.word_root}"'

    def __repr__(self):
        return f'"{self.word_root}" = {self.curated_sense}'


class Sense(models.Model):
    sense_uri = models.TextField(default="")
    sense_tree = models.ForeignKey(SenseTree, on_delete=models.CASCADE)

    def __str__(self):
        return self.sense_uri

    def __repr__(self):
        return self.sense_uri
