from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, null=True, blank=True)
    longurl = models.URLField()
    shorturl = models.URLField()
    modified = models.DateTimeField()
    user = models.ForeignKey(User)

    def __str__(self):
        return "{}".format(self.title)


class Click(models.Model):
    timestamp = models.DateTimeField()
    clicker = models.ForeignKey(User)
    bookmark = models.ForeignKey(Bookmark)

    def __str__(self):
        return "{}: {}".format(self.bookmark, self.timestamp)
