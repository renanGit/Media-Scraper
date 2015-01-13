from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % self.title