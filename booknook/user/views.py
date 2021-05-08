from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from user.models import BookNookUser, BookReview
from books.models import Book
from django.contrib.auth.decorators import login_required
from datetime import datetime
from random import random

def profile(request):
    user = request.user
    bnuser = BookNookUser.objects.get(ID=user.id)
    return render(request, "profile.html", {"bnuser": bnuser, "user": user})

def timeline(request):
    # reviews = BookReview.objects.all()
    books = Book.objects.all()
    user = request.user
    print(user.id)
    bnuser = BookNookUser.objects.get(ID=user.id)
    # booknookuser = BookNookUser.objects.get(user=request.user) 
    # TODO: change to booknookuser when the db migration is applied in templates as well
    return render(request, "timeline.html", {"books": books, "user": user, "bnuser": bnuser})
    # TODO: add booknookuser, reviews to render

def user_login(request):
    return render(request, "user_login.html", {})

def user_register(request):
    return render(request, "user_register.html", {})

def user_login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # bnuser = BookNookUser.objects.get(user=user)
        auth_login(request, user)
        return redirect("/timeline")
    else:
        return redirect("/login")

def user_register_view(request):
    # TODO: add duplicate control (carol)
    name = request.POST.get("name")
    username = request.POST.get("username")
    password = request.POST.get("password")
    userObj = User.objects.create(username=username, password=password)
    userObj.set_password(password)
    userObj.save()
    booknook_user = BookNookUser.objects.create(ID=userObj.id, name=name)
    booknook_user.save()
    return redirect('/register_complete')

def register_complete(request):
    return render(request, "register_complete.html", {})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


def new_review(request):
    user = request.user
    id = random()
    title = request.POST.get("review_title")
    title = request.POST.get("book_title")
    author = BookNookUser.objects.get(ID=user.id)
    book = Book.objects.get(title=title)
    time = datetime.now()
    review_content = request.POST.get("review_body")
    review = BookReview.objects.create(review_id=id, title=title, author=author, book_title=book, time=time, review_content=review_content)
    review.save()
    
    reviews = BookReview.objects.get(book_title=book)
    books = Book.objects.all()

    return render(request.META['HTTP_REFERER'], {reviews: reviews, books: books})


