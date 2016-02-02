from django.shortcuts import render, render_to_response, redirect ,HttpResponse
from .models import Video,User,Sequence, Correction
import os
from django.template import loader

def index(request, user_id):
    latest_video_list = Video.objects.order_by('name')[:5]
    context = {'latest_video_list': latest_video_list,
               'user_id':user_id}
    return render(request, 'index.html', context)

def video(request,user_id, video_id, edit):
    if Video.objects.filter(vid=video_id):
        if request.method == 'POST':
            for seq in Sequence.objects.filter(vid_id=video_id):
                new_con = request.POST.get('sub'+str(seq.sid))
                if seq.content != new_con:
                    corrs = Correction.objects.filter(sid_id=seq.sid)
                    if corrs:
                        ex = False
                        for corr in corrs:
                            uids = corr.uids.split(',')
                            if corr.new_content==new_con:
                                if not uids.__contains__(user_id):
                                    uids.append(user_id)
                                    corr.uids=','.join(uids)
                                    corr.save()
                                ex = True
                            else:
                                if uids.__contains__(user_id):
                                    uids.remove(user_id)
                                    corr.uids=','.join(uids)
                                    corr.save()
                        if not ex:
                            Correction(sid_id=seq.sid,vid_id=seq.vid_id,uids=user_id,new_content=new_con).save()
                    else:
                        Correction(sid_id=seq.sid,vid_id=seq.vid_id,uids=user_id,new_content=new_con).save()
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
                corrs = Correction.objects.filter(sid=sub.sid)
                if corrs:
                    for corr in corrs:
                        if corr.uids.split(',').__contains__(user_id):
                            sub.content = corr.new_content
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
            vttFile.close()
        subs_all = []
        for i in range(Sequence.objects.filter(vid_id=video_id,lang=idvideo.sub_langs.split(',')[0]).count()):
            subs = []
            for lang in idvideo.sub_langs.split(","):
                subs.append(Sequence.objects.filter(vid_id=video_id,lang=lang).order_by('start')[i])
            subs_all.append(subs)
        context = {'idvideo': idvideo,
                   'subs_all': subs_all,
                   'sub_langs': idvideo.sub_langs.split(","),
                   'edit': edit=="edit"}
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


def correction(request):
    changed = []
    correction_list = Correction.objects.filter(verified=False).order_by('uids')
    initial_sequence = []
    screator = []
    for c in correction_list:
        if Sequence.objects.get(sid=c.sid_id) not in initial_sequence:
            initial_sequence.append(Sequence.objects.get(sid=c.sid_id))
        users = c.uids.split(',')
        c.uids = int(users[0])
        if User.objects.get(uid=c.uids) not in screator:
            screator.append(User.objects.get(uid=c.uids))

    if request.method == 'POST':
        seq = ''
        for c in correction_list:
            seq = str(c.cid)
            if request.POST.get(seq) is not None:
                changed.append(request.POST.get(seq))

        for s in changed:
            corr = Correction.objects.get(cid=s)
            rootseq = Sequence.objects.get(sid=corr.sid_id)
            creator = corr.uids.split(',')
            sequence = Sequence(vid=corr.vid,lang=rootseq.lang,content=corr.new_content,start=rootseq.start,end=rootseq.end,creator_id=creator[0],rating=0)
            sequence.save()
            corr.verified=True
            corr.save()

        return redirect('/correction')

    template = loader.get_template('correction.html')
    context ={
        'correction_list': correction_list,
        'changed': changed,
        'initial_sequence': initial_sequence,
        'screator': screator,
    }
    return HttpResponse(template.render(context, request))
