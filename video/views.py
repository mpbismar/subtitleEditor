from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Video

def index(request):
    latest_video_list = Video.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.name for q in latest_video_list])
    return HttpResponse(output)

def video(request, video_id):
    return render_to_response('video.html')