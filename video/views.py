from django.shortcuts import render, render_to_response
from .models import Video

def index(request):
    latest_video_list = Video.objects.order_by('-pub_date')[:5]
    context = {'latest_video_list': latest_video_list}
    return render(request, 'index.html', context)

def video(request, video_id):
    video_name_list = Video.objects.select_related(Video, "name").filter(Video, "vid"==video_id)
    video_name = video_name_list[0]
    context = {'video_name': video_name}
    return render(request, 'video.html', context)

def login(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
    else:
        return render(request, 'login.html',{})


