from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, null=True, blank=True)
    longurl = models.URLField()
    shorturl = models.CharField(max_length=10)
    modified = models.DateTimeField()
    user = models.ForeignKey(User)

    def __str__(self):
        return "{}".format(self.title)

    def generate_short(self):
        '''Generates a shorturl for the bookmark.
        also validates to make sure it doesn't already exist.
        N = number of characters.
        string.ascii_uppercase + string.digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        '''
        import string
        import random
        N = 6
        short = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
        if Bookmark.objects.filter(shorturl=short).count() == 1:
            self.generate_short()
        else:
            self.shorturl = short


class Click(models.Model):
    timestamp = models.DateTimeField()
    clicker = models.ForeignKey(User, null=True)
    bookmark = models.ForeignKey(Bookmark)

    def __str__(self):
        return "{}: {}".format(self.bookmark, self.timestamp)
