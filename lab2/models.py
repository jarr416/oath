from django.db import models

class user(models.Model):
    fsID = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class foursquareinfo(models.Model):
    username = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    fs_id = models.CharField(max_length=200)