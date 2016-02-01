from django.conf.urls import patterns, include, url
from video import views
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subtitleEditor.views.home', name='home'),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^correction/$', views.correction, name='correction'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<user_id>[0-9]+)/', include('video.urls')),
    url(r'^admin/', admin.site.urls)

)

