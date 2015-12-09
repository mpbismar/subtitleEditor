from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subtitleEditor.views.home', name='home'),
    url(r'^video/', include('video.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
