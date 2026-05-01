from typing import TYPE_CHECKING

from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import LogInForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def login_user(request: HttpRequest) -> HttpResponse:
    post_data = request.POST if request.method == "POST" else None
    form = LogInForm(request=request, data=post_data)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request=request, user=user)
        return redirect(to="core:index")
    return render(
        request=request,
        template_name="authenticate/login.html",
        context={"date": None, "form": form},
    )


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect(to="members:login")

