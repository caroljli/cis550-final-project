from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from user.models import BookNookUser, BookReview, UserFollowers
from books.models import Book, BookFollowers
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from itertools import chain

def splash(request):
    if request.user.is_authenticated:
        books = Book.objects.all()
        logged_in = True
        try: 
            user = SocialAccount.objects.get(user=request.user)
            user_id = user.user.id
            name = user.extra_data.get('name')
            bio = "I am a Social Media user!"
            bnuser = BookNookUser.objects.create(ID=user_id, name=name, bio=bio)
        except ObjectDoesNotExist:
            user = request.user
            bnuser = BookNookUser.objects.get(ID=user.id)

        param_dict = { "param": bnuser.ID }
        reviews = BookReview.objects.raw('SELECT * FROM BookReview WHERE BOOK_TITLE IN (SELECT ID FROM BookFollowers WHERE FOLLOWER_ID = %(param)s)', param_dict)
        param_user = { "param": bnuser.ID }
        user_reviews = BookReview.objects.raw('SELECT * FROM BookReview WHERE AUTHOR IN (SELECT ID FROM UserFollowers WHERE FOLLOWER_ID = %(param)s)', param_user)

        return render(request, "timeline.html", {"books": books, "user": user, "bnuser": bnuser, "logged_in": logged_in, "reviews": reviews, "user_reviews": user_reviews})
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
    book_following = BookFollowers.objects.filter(follower_id=user_id)
    followers_length = len(followers)
    following_length = len(following)
    book_following_length = len(book_following)
    print(user_id)
    print(followers_length)
    print(following_length)
    return render(request, "profile.html", {"url": url, "bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews, "followers": followers, "following": following, "followers_length": followers_length, "following_length": following_length, "book_following": book_following, "book_following_length": book_following_length})

def user_profile(request, url=None):
    logged_in = True
    bnuser = BookNookUser.objects.filter(ID=url).first()
    user = User.objects.get(id=url)
    username = user.username
    reviews = BookReview.objects.filter(author=url)
    followers = UserFollowers.objects.filter(ID=url)
    following = UserFollowers.objects.filter(follower_id=url)
    book_following = BookFollowers.objects.filter(follower_id=url)
    followers_length = len(followers)
    following_length = len(following)
    book_following_length = len(book_following)
    try: 
        followers.get(follower_id=request.user.id)
        followed = True
    except ObjectDoesNotExist:
        followed = False
    print(url)
    print(followers_length)
    print(following_length)
    print(book_following_length)
    print(followed)
    return render(request, "profile.html", {"url": url, "bnuser": bnuser, "user": user, "logged_in": logged_in, "username": username, "reviews": reviews, "followers": followers, "following": following, "followers_length": followers_length, "following_length": following_length, "followed": followed, "book_following": book_following, "book_following_length": book_following_length})

# def timeline(request):
#     books = Book.objects.all()
#     logged_in = True
#     try: 
#         user = SocialAccount.objects.get(user=request.user)
#         user_id = user.user.id
#         name = user.extra_data.get('name')
#         bio = "I am a Google user!"
#         bnuser = BookNookUser.objects.create(ID=user_id, name=name, bio=bio)
#     except ObjectDoesNotExist:
#         user = request.user
#         bnuser = BookNookUser.objects.get(ID=user.id)

#     # following books
#     # TODO: OPTIMIZE THIS QUERY (and write as sql query)
#     # following_book_ids_list = BookFollowers.objects.filter(follower_id=bnuser.ID).values_list('ID', flat=True)
#     # following_books_ids_list = BookFollowers.objects.raw('SELECT ID FROM BookFollowers WHERE FOLLOWER_ID = bnuser.ID')
#     print(bnuser.ID)
#     # print(following_books_ids_list.__len__)
#     # following_book_ids = [str(i) for i in following_book_ids_list]
#     # print(following_book_ids)
#     param_dict = { "param": bnuser.ID }
#     reviews = BookReview.objects.raw('SELECT * FROM BookReview WHERE BOOK_TITLE IN (SELECT ID FROM BookFollowers WHERE FOLLOWER_ID = %(param)s)', param_dict)
#     # reviews = BookReview.objects.raw('SELECT * FROM BookReview WHERE BOOK_TITLE IN (SELECT ID FROM BookFollowers WHERE FOLLOWER_ID = 74)')
#     # reviews = BookReview.objects.filter(book_title__in=following_book_ids)
#     # print(reviews.values_list('book_name', flat=True))

#     # following users
#     # TODO: OPTIMIZE THIS QUERY (and write as sql query)
#     # print(bnuser.ID)
#     param_user = { "param": bnuser.ID }
#     user_reviews = BookReview.objects.raw('SELECT * FROM BookReview WHERE AUTHOR IN (SELECT ID FROM UserFollowers WHERE FOLLOWER_ID = %(param)s)', param_user)

#     # following_user_ids_list = UserFollowers.objects.filter(follower_id=bnuser.ID).values_list('ID', flat=True)
#     # following_user_ids = [str(i) for i in following_user_ids_list]
#     # user_reviews = BookReview.objects.filter(author__in=following_user_ids)
#     # print(user_reviews.values_list('book_name', flat=True))

#     return render(request, "timeline.html", {"books": books, "user": user, "bnuser": bnuser, "logged_in": logged_in, "reviews": reviews, "user_reviews": user_reviews})

def user_login(request):
    return render(request, "user_login.html", {})

def user_register(request):
    return render(request, "user_register.html", {})

def user_login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
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
    review_title = request.POST.get("review_title")
    book_title = request.POST.get("book_title")
    author_name = BookNookUser.objects.filter(ID=user.id).first().name
    author = BookNookUser.objects.filter(ID=user.id).first().ID
    print(Book.objects.filter(title__icontains = str(book_title)).first().ID)
    book_id = Book.objects.filter(title__icontains = str(book_title)).first().ID

    time = datetime.now()
    review_content = request.POST.get("review_body")
    review = BookReview.objects.create(ID=review_id, review_title=review_title, author=author, book_title=book_id, time=time, review_content=review_content, book_name=book_title, author_name=author_name)
    review.save()
    # return redirect("/timeline")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_user(request):
    print(request.POST.get('follow_user'))
    print(request.user.id)

    user = request.user
    bnfollower = BookNookUser.objects.filter(ID=user.id).first()
    if 'follow_user' in request.POST:
        to_follow = BookNookUser.objects.get(ID=request.POST.get('follow_user'))
        UserFollowers.objects.create(ID=to_follow.ID, name=to_follow.name, follower_id=bnfollower.ID, follower_name=bnfollower.name)
        print(bnfollower.name)
    else:
        UserFollowers.objects.filter(ID=request.POST.get('unfollow_user')).delete()
    # return redirect("/profile")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))