from django.db import models

class Video(models.Model):
    vid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    lang = models.CharField(max_length=5)
    sub_langs = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now=True)

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    n_apr = models.PositiveIntegerField(default=0)
    n_cor = models.PositiveIntegerField(default=0)
    password  = models.CharField(max_length=40)

class Sequence(models.Model):
    sid = models.AutoField(primary_key=True)
    vid = models.ForeignKey(Video,to_field="vid")
    lang = models.CharField(max_length=5)
    content = models.CharField(max_length=150)
    start = models.PositiveIntegerField(serialize=False)
    end = models.PositiveIntegerField(serialize=False)

class Correction(models.Model):
    vid = models.ForeignKey(Video,to_field="vid")
    sid = models.ForeignKey(Sequence,to_field="sid")
    uids = models.CharField(max_length=500)
    new_content = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now=True)