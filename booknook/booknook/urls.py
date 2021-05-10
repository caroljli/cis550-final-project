"""booknook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books.views import book_directory, authors, mostreviews, book, follow_book
from user.views import profile, timeline, user_login, user_login_view, logout_view, register_complete, user_register, user_register_view, new_review, user_profile, follow_user, splash


urlpatterns = [
    # general
    path('admin/', admin.site.urls),
    path('', splash, name="splash"),
    path('logout_view/', logout_view, name="logout_view"),

    # user pages
    path('authors/', authors, name="authors"),
    path('mostreviews/', mostreviews, name="mostreviews"),
    path('profile/', profile, name="profile"),
    path('profile/<slug:url>', user_profile, name="profile"),
    path('timeline/', timeline, name="timeline"),

    # user auth
    path('user_login_view/', user_login_view, name="user_login_view"),
    path('login/', user_login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('register/', user_register, name="user_register"),
    path('register_view/', user_register_view, name="user_register_view"),
    path('register_complete/', register_complete, name="register_complete"),

    # user book reviews
    path('new_review/', new_review, name="new_review"),

    # book pages
    path('books/', book_directory, name="books"),
    path('book/<slug:url>', book, name="book"),

    # following
    path('follow_user/', follow_user, name="follow_user"),
    path('follow_book/', follow_book, name="follow_book")
]
