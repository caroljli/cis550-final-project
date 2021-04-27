from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import template

class BookNookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # school = models.CharField(max_length=200)
    # bio = models.TextField()
    # time = models.DateTimeField(auto_now=True, null=True)
    # following = models.ManyToManyField(Follow, related_name='following', null=True)
    # picture = models.CharField(max_length=600, null=True)
    # is_student = True
    # is_restaurant = False