from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<video_id>[0-9]+)/?$', views.video, name='video'),
    url(r'^index$', views.index, name='index'),
    url(r'^correction/?$', views.correction, name='correction'),
    url(r'^statistics/?$', views.statistics, name='statistics')

]
