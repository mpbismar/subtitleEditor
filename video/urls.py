from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^(?P<video_id>[0-9]+)/$', views.video, name='video'),
    url(r'^penis$', views.index, name='index')

]
