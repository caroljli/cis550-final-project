from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from user.models import BookNookUser, BookReview
from books.models import Book
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from datetime import datetime
from random import random
from django.core.exceptions import ObjectDoesNotExist

def profile(request):
    logged_in = True
    try: 
        user = SocialAccount.objects.get(user=request.user)
        user_id = user.user.id
        username = user.extra_data.get('email').split('@')[0]
    except ObjectDoesNotExist:
        user = request.user
        user_id = user.id
        username = user.username
    bnuser = BookNookUser.objects.filter(ID=user_id).first()
    reviews = BookReview.objects.filter(author=user_id)
    print(user_id)
    return render(request, "profile.html", {"bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews})

def user_profile(request, url=None):
    logged_in = True
    bnuser = BookNookUser.objects.filter(ID=url).first()
    user = User.objects.get(id=url)
    username = user.username
    reviews = BookReview.objects.filter(author=url)
    print(url)
    return render(request, "profile.html", {"bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews})

def timeline(request):
    # reviews = BookReview.objects.all()
    books = Book.objects.all()
    logged_in = True
    try: 
        user = SocialAccount.objects.get(user=request.user)
        user_id = user.user.id
        name = user.extra_data.get('name')
        bnuser = BookNookUser.objects.create(ID=user_id, name=name)
    except ObjectDoesNotExist:
        user = request.user
        bnuser = BookNookUser.objects.get(ID=user.id)
    reviews = BookReview.objects.all()
    return render(request, "timeline.html", {"books": books, "user": user, "bnuser": bnuser, "logged_in": logged_in, "reviews": reviews})

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
    name = request.POST.get("name")
    username = request.POST.get("username")
    password = request.POST.get("password")
    bio = request.POST.get("bio") # TODO: add bio
    try:
        User.objects.get(username=username)
        return redirect('/register')
    except ObjectDoesNotExist:
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
    # review_id = random()
    title = request.POST.get("review_title")
    book_title = request.POST.get("book_title")
    author = BookNookUser.objects.get(ID=user.id).ID
    book_id = Book.objects.get(title=book_title).ID
    time = datetime.now()
    review_content = request.POST.get("review_body")
    review = BookReview.objects.create(title=title, author=author, book_title=book_id, time=time, review_content=review_content)
    review.save()
    
    # reviews = BookReview.objects.get(book_title=book_id)
    # books = Book.objects.all()

    return render(request.META['HTTP_REFERER'], {})


