from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, HttpResponse
from .models import Video, UserStats, Sequence, Correction
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader


def index(request):
    latest_video_list = Video.objects.order_by('name')[:5]
    context = {'latest_video_list': latest_video_list}
    return render(request, 'index.html', context)


def video(request, video_id):
    user_id = request.user.id
    if Video.objects.filter(vid=video_id):
        idvideo = Video.objects.get(vid=video_id)
        times = Sequence.objects.filter(vid_id=video_id, lang=idvideo.sub_langs.split(',')[0])\
            .order_by('start').values('start','end').distinct()
        if request.method == 'POST':
            if request.POST.get('subedit'):
                new_con = request.POST.get('subedit')
                start = request.POST.get('start')
                exists = False
                refer_seq = Sequence.objects.filter(vid_id=video_id,start=start).order_by('creator_id').first()
                for seq in Sequence.objects.filter(vid_id=video_id,start=start):
                    if seq.content == new_con:
                        exists = True
                if not exists:
                    corrs = Correction.objects.filter(vid_id=video_id,sid_id=refer_seq.sid)
                    if corrs:
                        corr_exists = False
                        for corr in corrs:
                            uids = corr.uids.split(',')
                            if corr.new_content==new_con:
                                if not uids.__contains__(user_id):
                                    uids.append(user_id)
                                    corr.uids=','.join(uids)
                                    corr.save()
                                corr_exists = True
                            else:
                                if uids.__contains__(user_id):
                                    uids.remove(user_id)
                                    if not uids:
                                        corr.delete() #doesn't work somehow
                                    corr.uids=','.join(uids)
                                    corr.save()
                        if not corr_exists:
                            Correction(sid_id=refer_seq.sid,vid_id=video_id,uids=user_id,new_content=new_con).save()
                    else:
                        Correction(sid_id=refer_seq.sid,vid_id=video_id,uids=user_id,new_content=new_con).save()
            else:
                lang_id = request.POST.get('lang')
                lang = idvideo.sub_langs.split(',')[int(lang_id)]
                seqs = Sequence.objects.filter(vid_id=video_id, lang=lang).order_by('start')
                sub_id = 0
                version_id = 0
                start = seqs[0].start
                for seq in seqs:
                    if seq.start != start:
                        sub_id+=1
                        start = seq.start
                        version_id = 0
                    if version_id == int(request.POST.get('r'+str(sub_id))):
                        seq.rating += 1
                        seq.save(force_update=True)
                    version_id += 1

        path = "video/static/subtitles/vtt/"
        if not os.path.exists(path):
            os.makedirs(path)
        for lang in idvideo.sub_langs.split(","):
            subs = Sequence.objects.filter(vid_id=video_id, lang=lang)
            vttFile = open(os.path.join(path, idvideo.name + "_" + lang + ".vtt"), "w")
            vttFile.truncate()
            vttFile.write("WEBVTT\n\n")
            i = 0
            for time in times:
                refer_sub = Sequence.objects.filter(vid_id=video_id, lang=lang, start=time.get("start", 0))\
                    .order_by('creator_id').first()
                sub = Sequence.objects.filter(vid_id=video_id, lang=lang, start=time.get("start", 0)).order_by('rating').last()
                corrs = Correction.objects.filter(sid_id=refer_sub.sid)
                if corrs:
                    for corr in corrs:
                        if corr.uids.split(',').__contains__(user_id):
                            sub.content = corr.new_content
                i += 1
                stime = str(sub.start / 1000 / 60 / 60).zfill(2) + ":"
                stime += str(sub.start / 1000 / 60 % 60).zfill(2) + ":"
                stime += str(sub.start / 1000 % 60).zfill(2) + "."
                stime += str(sub.start % 1000).zfill(3)

                etime = str(sub.end / 1000 / 60 / 60).zfill(2) + ":"
                etime += str(sub.end / 1000 / 60 % 60).zfill(2) + ":"
                etime += str(sub.end / 1000 % 60).zfill(2) + "."
                etime += str(sub.end % 1000).zfill(3)

                vttFile.write(str(i) + "\n")
                vttFile.write(stime + " --> " + etime + "\n")
                vttFile.write(sub.content + "\n\n")
            vttFile.close()
        subs_all = []
        max_versions = 0
        for lang in idvideo.sub_langs.split(","):
            seqs = Sequence.objects.filter(vid_id=video_id, lang=lang).order_by('start')
            subs = []
            versions = []
            start = seqs[0].start
            for seq in seqs:
                if seq.start != start:
                    if versions.__len__() > max_versions:
                        max_versions = versions.__len__()
                    subs.append(versions)
                    versions = []
                    start = seq.start
                versions.append(seq)
            subs.append(versions)
            subs_all.append(subs)

        context = {'idvideo': idvideo,
                   'subs_all': subs_all,
                   'sub_langs': idvideo.sub_langs.split(","),
                   'times': times,
                   'nseq': times.__len__(),
                   'maxseq': range(max_versions)}
        return render(request, 'video.html', context)
    else:
        return redirect('/' + str(user_id) + '/index')


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname = request.POST.get('username')
        pw = request.POST.get('password')
        user = User.objects.create_user(uname, '', pw)
        user.save()
        nuser = authenticate(username=uname, password=pw)
        login(request, nuser)
        return redirect('/index')

    return render(request, 'register.html', {'message':''})
"""
        if not (User.objects.filter(name=uname)):
            user = User(name=uname, password=pw)
            user.save()
            user = User.objects.get(name=uname)
            return redirect('/' + str(user.uid) + '/index')
        else:
            return render(request, 'register.html',
                          {'message': 'This username is already taken. Select a different one.'})

    else:
        return render(request, 'register.html', {'message': ''})
"""

def login_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(username=uname, password=pw)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/index')
    return render(request, 'login.html', {'message': ''})
"""        if User.objects.filter(name=uname):
            user = User.objects.get(name=uname)
            if user.password == pw:
                return redirect('/' + str(user.uid) + '/index')
        return render(request, 'login.html', {'message': 'Unknown combination of username and password'})
    else:
        return render(request, 'login.html', {'message': ''})
"""

def logout_user(request):
    logout(request)
    return redirect('/')

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
        if User.objects.get(id=c.uids) not in screator:
            screator.append(User.objects.get(id=c.uids))

    if request.method == 'POST':
        seq = ''
        for c in correction_list:
            seq = str(c.cid)
            if request.POST.get(seq) is not None:
                changed.append(request.POST.get(seq))

        for s in changed:
            corr = Correction.objects.get(cid=s)
            if 'verify' in request.POST:
                rootseq = Sequence.objects.get(sid=corr.sid_id)
                creator = corr.uids.split(',')
                sequence = Sequence(vid=corr.vid, lang=rootseq.lang, content=corr.new_content, start=rootseq.start,
                                    end=rootseq.end, creator_id=creator[0], rating=0)
                sequence.save()
            corr.verified = True
            corr.save()

        return redirect('/correction')

    context = {
        'correction_list': correction_list,
        'changed': changed,
        'initial_sequence': initial_sequence,
        'screator': screator,
    }
    return render(request, 'correction.html',context)

def statistics(request):
    users_rate = User.objects.exclude(n_rate = 0).order_by('-n_rate')[:10]
    users_corr = User.objects.exclude(n_cor = 0).order_by('-n_cor')[:10]
    context = {
        'users_rate': users_rate,
        'users_corr': users_corr
    }
    return render(request, 'statistic.html',context)
