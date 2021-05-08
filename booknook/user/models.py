from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import template
from books.models import Book

class BookNookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # bio = models.TextField(null=True)
    # time = models.DateTimeField(auto_now=True, null=True)
    # following = models.ManyToManyField(Follow, related_name='following', null=True)gcm
    #class Meta:
       # db_table = "USERS"

class BookReview(models.Model):
    title = models.TextField()
    #author = models.OneToOneField(BookNookUser, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    book_title = models.OneToOneField(Book, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, null=True)
    review_content = models.TextField()
    #class Meta:
       # db_table = "REVIEWS"
