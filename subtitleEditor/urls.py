from django.conf.urls import patterns, include, url
from video import views
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subtitleEditor.views.home', name='home'),
    url(r'^$', views.login_user, name='login'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^', include('video.urls')),
    url(r'^admin/', admin.site.urls)

)

