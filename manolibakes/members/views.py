from typing import TYPE_CHECKING

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LogInForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:index")
    return render(request, "authenticate/login.html", {"date": None, "form": LogInForm})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("members:login")
