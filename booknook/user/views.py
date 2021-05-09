from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from user.models import BookNookUser, BookReview, UserFollowers
from books.models import Book
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

def splash(request):
    if request.user.is_authenticated:
        books = Book.objects.all()
        logged_in = True
        try: 
            user = SocialAccount.objects.get(user=request.user)
            user_id = user.user.id
            name = user.extra_data.get('name')
            bio = "I am a Google user!"
            bnuser = BookNookUser.objects.create(ID=user_id, name=name, bio=bio)
        except ObjectDoesNotExist:
            user = request.user
            bnuser = BookNookUser.objects.get(ID=user.id)
        reviews = BookReview.objects.all()
        return render(request, "timeline.html", {"books": books, "user": user, "bnuser": bnuser, "logged_in": logged_in, "reviews": reviews})
    else:
	    return render(request, "splash.html", {})
    # return render(request, "splash.html", {})

def profile(request):
    logged_in = True
    url = None
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
    followers = UserFollowers.objects.filter(ID=user_id)
    following = UserFollowers.objects.filter(follower_id=user_id)
    followers_length = len(followers)
    following_length = len(following)
    print(user_id)
    print(followers_length)
    print(following_length)
    return render(request, "profile.html", {"url": url, "bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews, "followers": followers, "following": following, "followers_length": followers_length, "following_length": following_length})

def user_profile(request, url=None):
    logged_in = True
    bnuser = BookNookUser.objects.filter(ID=url).first()
    user = User.objects.get(id=url)
    username = user.username
    reviews = BookReview.objects.filter(author=url)
    followers = UserFollowers.objects.filter(ID=url)
    following = UserFollowers.objects.filter(follower_id=url)
    followers_length = len(followers)
    following_length = len(following)
    try: 
        followers.get(follower_id=request.user.id)
        followed = True
    except ObjectDoesNotExist:
        followed = False
    print(url)
    print(followers_length)
    print(following_length)
    print(followed)
    return render(request, "profile.html", {"url": url, "bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews, "followers": followers, "following": following, "followers_length": followers_length, "following_length": following_length, "followed": followed})

def timeline(request):
    # reviews = BookReview.objects.all()
    books = Book.objects.all()
    logged_in = True
    try: 
        user = SocialAccount.objects.get(user=request.user)
        user_id = user.user.id
        name = user.extra_data.get('name')
        bio = "I am a Google user!"
        bnuser = BookNookUser.objects.create(ID=user_id, name=name, bio=bio)
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
        booknook_user = BookNookUser.objects.create(ID=userObj.id, name=name, bio=bio)
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
    review_id = random.randint(1,1000)
    # print(review_id)
    review_title = request.POST.get("review_title")
    # print(review_title)
    book_title = request.POST.get("book_title")
    # print(book_title)
    author_name = BookNookUser.objects.filter(ID=user.id).first().name
    author = BookNookUser.objects.filter(ID=user.id).first().ID

    # print("author worked")

    # print(Book.objects.filter(title__icontains = str(book_title)))
    print(Book.objects.filter(title__icontains = str(book_title)).first().ID)

    # print ("break")
    book_id = Book.objects.filter(title__icontains = str(book_title)).first().ID

    time = datetime.now()
    review_content = request.POST.get("review_body")
    review = BookReview.objects.create(ID=review_id, review_title=review_title, author=author, book_title=book_id, time=time, review_content=review_content, book_name=book_title, author_name=author_name)
    review.save()
    # return redirect("/timeline")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_user(request, url=None):
    print(request.POST.get('follow_user'))
    print(request.user.id)

    user = request.user
    bnfollower = BookNookUser.objects.filter(ID=user.id).first()
    if 'follow_user' in request.POST:
        to_follow = BookNookUser.objects.get(ID=request.POST.get('follow_user'))
        UserFollowers.objects.create(ID=to_follow.ID, name=to_follow.name, follower_id=bnfollower.ID, follower_name=bnfollower.name)
        print(bnfollower.name)
    else:
        # to_unfollow = BookNookUser.objects.get(ID=request.POST.get('unfollow_user'))
        UserFollowers.objects.filter(ID=request.POST.get('unfollow_user')).delete()
    # return redirect("/profile")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))