from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import LogInForm


def login_user(request):
    if request.method == "POST":
        print("post request!")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user authenticated!")
            login(request, user)
            print("user logged in!")
            return redirect("core:index")
    return render(request, "authenticate/login.html", {"date": None, "form": LogInForm})


def logout_user(request):
    logout(request)
    return redirect("members:login")
