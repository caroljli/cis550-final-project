from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import template
from books.models import Book

class BookNookUser(models.Model):
    ID = models.IntegerField()
    # userObj = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=20)
    # time = models.DateTimeField(auto_now=True, null=True)
    # following = models.ManyToManyField(Follow, related_name='following', null=True)
    class Meta:
        db_table = "BOOKNOOKUSER"

class BookReview(models.Model):
    ID = models.IntegerField()
    # review_id = models.IntegerField(primary_key=True, default=0)
    review_title = models.TextField()
    # author = models.ForeignKey(BookNookUser, on_delete=models.CASCADE)
    author = models.IntegerField()
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    #author = models.CharField(max_length=200)
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_title = models.IntegerField()
    time = models.DateTimeField(auto_now=True, null=True)
    review_content = models.CharField(max_length=200)
    
    class Meta:
       db_table = "BOOKREVIEW"
    #    abstract = True

class UserFollowers(models.Model):
    ID = models.IntegerField()
    name = models.CharField(max_length=200)
    follower_id = models.IntegerField()
    follower_name = models.CharField(max_length=200)

    class Meta:
        db_table = "USERFOLLOWERS"