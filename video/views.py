from django.shortcuts import render, render_to_response, redirect ,HttpResponse
from .models import Video,User

def index(request, user_id):
    latest_video_list = Video.objects.order_by('-pub_date')[:5]
    context = {'latest_video_list': latest_video_list,
               'user_id':user_id}
    return render(request, 'index.html', context)

def video(request,user_id, video_id):
    if Video.objects.filter(vid=video_id):
        idvideo = Video.objects.get(vid=video_id)
        context = {'idvideo': idvideo}
        return render(request, 'video.html', context)
    else:
        return redirect('/'+str(user_id)+'/index')

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname=request.POST.get('username')
        pw=request.POST.get('password')

        if not(User.objects.filter(name=uname)):
            user=User(name=uname,password=pw)
            user.save()
            user=User.objects.get(name=uname)
            return redirect('/'+str(user.uid)+'/index')
        else:
            return render(request, 'register.html', {'message': 'This username is already taken. Select a different one.'})

    else :
        return render(request, 'register.html', {'message': ''})

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname=request.POST.get('username')
        pw=request.POST.get('password')

        if User.objects.filter(name=uname):
            user=User.objects.get(name=uname)
            if user.password==pw:
                return redirect('/'+str(user.uid)+'/index')
        return render(request, 'login.html',{'message':'Unknown combination of username and password'})


    else :
        return render(request, 'login.html',{'message':''})

