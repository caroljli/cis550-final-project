from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import template
from books.models import Book

class BookNookUser(models.Model):
    ID = models.IntegerField()
    # userObj = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # bio = models.TextField(null=True)
    # time = models.DateTimeField(auto_now=True, null=True)
    # following = models.ManyToManyField(Follow, related_name='following', null=True)gcm
    class Meta:
        db_table = "BOOKNOOKUSER"

class BookReview(models.Model):
    review_id = models.IntegerField(primary_key=True, default=0)
    title = models.TextField()
    author = models.ForeignKey(BookNookUser, on_delete=models.CASCADE)
    #author = models.CharField(max_length=200)
    book_title = models.OneToOneField(Book, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, null=True)
    review_content = models.CharField(max_length=200)
    class Meta:
       db_table = "BOOKREVIEW"
