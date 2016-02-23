import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Video, UserStats, Sequence, Correction


@login_required
def index(request):
    latest_video_list = Video.objects.order_by('name')[:5]
    context = {'latest_video_list': latest_video_list}
    return render(request, 'index.html', context)


@login_required
def video(request, video_id):
    user_id = request.user.id
    if Video.objects.filter(vid=video_id):
        idvideo = Video.objects.get(vid=video_id)
        times = Sequence.objects.filter(vid_id=video_id, lang=idvideo.sub_langs.split(',')[0]) \
            .order_by('start').values('start', 'end').distinct()
        if not UserStats.objects.filter(uid_id=user_id):
            userstat = UserStats.objects.create(n_rate=0, n_corr=0, uid_id=user_id)
            userstat.save(force_update=True)
        else:
            userstat = UserStats.objects.get(uid_id=user_id)
        if request.method == 'POST':
            if request.POST.get('subedit'):
                new_con = request.POST.get('subedit')
                start = request.POST.get('start')
                c_lang = request.POST.get('lang')
                refer_seq = Sequence.objects.filter(vid_id=video_id, start=start, lang=c_lang).order_by(
                    'creator_id').first()
                corrs = Correction.objects.filter(vid_id=video_id, sid_id=refer_seq.sid)
                if corrs:
                    corr_exists = False
                    for corr in corrs:
                        uids = corr.uids.split(',')
                        if corr.new_content == new_con:
                            if not uids.__contains__(str(user_id)):
                                uids.append(str(user_id))
                                corr.uids = ','.join(uids)
                                corr.save()
                            corr_exists = True
                        else:
                            if uids.__contains__(str(user_id)):
                                uids.remove(str(user_id))
                                if uids.__len__() == 0:
                                    Correction.objects.filter(cid=corr.cid).delete()
                                else:
                                    corr.uids = ','.join(uids)
                                    corr.save()
                    if not corr_exists:
                        Correction(sid_id=refer_seq.sid, vid_id=video_id, uids=str(user_id), new_content=new_con).save()
                else:
                    Correction(sid_id=refer_seq.sid, vid_id=video_id, uids=str(user_id), new_content=new_con).save()

            else:
                c_lang = request.POST.get('lang')
                ratings = request.POST.get('ratefield')
                ratings = ratings.split(',')
                ratings = [int(x) for x in ratings]
                del ratings[-1]
                seqs = Sequence.objects.filter(vid_id=video_id, lang=c_lang).order_by('start')
                seqlist = []
                counter = 0
                for rate in ratings:
                    if rate > -1:
                        seqlist.append(seqs[counter + rate])
                        i = 1
                        while (counter + i + rate < seqs.__len__() & seqs[counter + rate].start == seqs[
                                    counter + rate + i].start):
                            i += 1
                        counter = counter + rate + i
                    else:
                        i = 1
                        while counter + i < seqs.__len__() & seqs[counter].start == seqs[counter + i].start:
                            i += 1
                        counter = counter + i

                for s in seqlist:
                    sequence = Sequence.objects.get(sid=s.sid)
                    sequence.rating += 1
                    sequence.save(force_update=True)
                    userstat.n_rate += 1
                    userstat.save(force_update=True)

                    # for seq in seqs:
                    #     if seq.start != start:
                    #         sub_id += 1
                    #         start = seq.start
                    #         version_id = 0
                    #     if version_id == int(request.POST.get('r' + str(sub_id))):
                    #         seq.rating += 1
                    #         seq.save(force_update=True)
                    #         userstat.n_rate += 1
                    #         userstat.save(force_update=True)
                    #     version_id += 1

        path = "video/static/subtitles/vtt/"
        if not os.path.exists(path):
            os.makedirs(path)
        for lang in idvideo.sub_langs.split(","):
            vtt_file = open(os.path.join(path, idvideo.name + "_" + lang + ".vtt"), "w")
            vtt_file.truncate()
            vtt_file.write("WEBVTT\n\n")
            i = 0
            for time in times:
                refer_sub = Sequence.objects.filter(vid_id=video_id, lang=lang, start=time.get("start", 0)) \
                    .order_by('creator_id').first()
                sub = Sequence.objects.filter(vid_id=video_id, lang=lang, start=time.get("start", 0)).order_by(
                        'rating').last()
                corrs = Correction.objects.filter(sid_id=refer_sub.sid)
                if corrs:
                    for corr in corrs:
                        if corr.uids.split(',').__contains__(str(user_id)):
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

                vtt_file.write(str(i) + "\n")
                vtt_file.write(stime + " --> " + etime + "\n")
                vtt_file.write(sub.content + "\n\n")
            vtt_file.close()
        subs_all = []
        subs_dict = []
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
                versions.append(str(seq.content))
            subs.append(versions)
            subs_all.append(subs)
            subs_dict.append(lang)

        context = {'idvideo': idvideo,
                   'subs_all': subs_all,
                   'sub_langs': idvideo.sub_langs.split(","),
                   'subs_dict': subs_dict,
                   'test': [1, 2, 3],
                   'test2': [['1', '2'], ['3', '4'], ['5', '6']],
                   'times': times,
                   'nseq': times.__len__(),
                   'maxseq': range(max_versions)}
        return render(request, 'video.html', context)
    else:
        return redirect('/index')


# def importVtt(request):
# TODO:

# def importVideo(request):
# TODO:


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

    return render(request, 'register.html', {'message': ''})


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


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
@permission_required('auth.admin_view', '/index')
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
        if UserStats.objects.get(id=c.uids) not in screator:
            screator.append(UserStats.objects.get(id=c.uids))

    for sc in screator:
        sc.id = User.objects.get(id=sc.uid_id)

    if request.method == 'POST':
        for c in correction_list:
            seq = str(c.cid)
            if request.POST.get(seq) is not None:
                changed.append(request.POST.get(seq))

        for s in changed:
            corr = Correction.objects.get(cid=s)
            if 'verify' in request.POST:
                rootseq = Sequence.objects.get(sid=corr.sid_id)
                creator = corr.uids.split(',')
                userstat = UserStats.objects.get(uid_id=creator[0])
                userstat.n_corr += 1
                userstat.save(force_update=True)
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
    return render(request, 'correction.html', context)


@login_required
@permission_required('auth.admin_view', '/index')
def statistics(request):
    users_rate = UserStats.objects.exclude(n_rate=0).order_by('-n_rate')[:10]
    for ur in users_rate:
        ur.id = User.objects.get(id=ur.uid_id).username
    users_corr = UserStats.objects.exclude(n_corr=0).order_by('-n_corr')[:10]
    for uc in users_corr:
        uc.id = User.objects.get(id=uc.uid_id).username
    context = {
        'users_rate': users_rate,
        'users_corr': users_corr,
    }
    return render(request, 'statistic.html', context)
