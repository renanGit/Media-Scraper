from django.db import models

class Movie(models.Model):
    title = models.CharField()

    def __unicode__(self):
        return u'%s' % self.title