from django.db import models

class User(models.Model):
    uid = models.PositiveIntegerField(primary_key=True, db_index=True, unique=True)
    name = models.CharField(max_length=40)
    n_votes = models.PositiveIntegerField(default=0)
    n_corr = models.PositiveIntegerField(default=0)

class Sequence(models.Model):
    sid = models.PositiveIntegerField(primary_key=True, db_index=True, unique=True)
    vid = models.PositiveIntegerField(serialize=False)
    lang = models.CharField(max_length=5)
    content = models.CharField(max_length=150)
    start = models.PositiveIntegerField(serialize=False)
    end = models.PositiveIntegerField(serialize=False)

class Video(models.Model):
    vid = models.PositiveIntegerField(primary_key=True, db_index=True, unique=True)
    name = models.CharField(max_length=40)
    lang = models.CharField(max_length=5)
    sub_langs = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now_add=True)

class Correction(models.Model):
    vid = models.PositiveIntegerField(serialize=False)
    sid = models.PositiveIntegerField(serialize=False)
    uids = models.CharField(max_length=500)
    new_content = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now_add=True)