from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MediaSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^scraper/$', include('scraper.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
