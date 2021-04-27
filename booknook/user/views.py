from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from user.models import BookNookUser
from django.contrib.auth.decorators import login_required

def profile(request):
    return render(request, "profile.html", {})

def timeline(request):
    return render(request, "timeline.html", {})

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
    user = User.objects.create(username=username, password=password)
    user.set_password(password)
    user.save()
    BookNookUser.objects.create(user=user, name=name)
    return redirect('/register_complete')

def register_complete(request):
    return render(request, "register_complete.html", {})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")