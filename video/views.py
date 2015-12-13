from django.shortcuts import render, render_to_response, redirect ,HttpResponse
from .models import Video,User,Sequence
import os

def index(request, user_id):
    latest_video_list = Video.objects.order_by('-pub_date')[:5]
    context = {'latest_video_list': latest_video_list,
               'user_id':user_id}
    return render(request, 'index.html', context)

def video(request,user_id, video_id):
    if Video.objects.filter(vid=video_id):
        idvideo = Video.objects.get(vid=video_id)
        path = "video/static/subtitles/vtt/"
        if not os.path.exists(path):
            os.makedirs(path)
        for lang in idvideo.sub_langs.split(","):
            subs = Sequence.objects.filter(vid_id=video_id,lang=lang)
            vttFile = open(os.path.join(path,idvideo.name+"_"+lang+".vtt"),"w")
            vttFile.truncate()
            vttFile.write("WEBVTT\n\n")
            i = 0
            for sub in subs:
                i += 1
                stime = str(sub.start/1000/60/60).zfill(2)+":"
                stime += str(sub.start/1000/60%60).zfill(2)+":"
                stime += str(sub.start/1000%60).zfill(2)+"."
                stime += str(sub.start%1000).zfill(3)

                etime = str(sub.end/1000/60/60).zfill(2)+":"
                etime += str(sub.end/1000/60%60).zfill(2)+":"
                etime += str(sub.end/1000%60).zfill(2)+"."
                etime += str(sub.end%1000).zfill(3)

                vttFile.write(str(i)+"\n")
                vttFile.write(stime+" --> "+etime+"\n")
                vttFile.write(sub.content+"\n\n")
            vttFile.flush()
            vttFile.close()
        context = {'idvideo': idvideo,
                   'sub_langs': idvideo.sub_langs.split(",")}
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

