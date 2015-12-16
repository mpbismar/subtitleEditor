from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<video_id>[0-9]+)/(?P<edit>[a-z]*)/?$', views.video, name='video'),
    url(r'^index$', views.index, name='index')

]

