from django.conf.urls import patterns, url
from scraper.views import *

urlpatterns = patterns('',
    url(r'^$', welcome),
    url(r'^search/$', search),
)
