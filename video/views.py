from django.shortcuts import render, render_to_response, redirect
from .models import Video,User

def index(request, user_id):
    latest_video_list = Video.objects.order_by('-pub_date')[:5]
    context = {'latest_video_list': latest_video_list}
    return render(request, 'index.html', context)

def video(request,user_id, video_id):
    idvideo = Video.objects.filter(vid=video_id)
    context = {'idvideo': idvideo}
    return render(request, 'video.html', context)

def login(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname=request.POST.get('username')

        if not(User.objects.filter(name=uname)):
            user=User(name=uname)
            user.save()
            user=User.objects.get(name=uname)
            return redirect('/'+str(user.uid)+'/index')


        else:
            user=User.objects.get(name=uname)
            return redirect('/'+str(user.uid)+'/index')

    else :
        return render(request, 'login.html',{})

