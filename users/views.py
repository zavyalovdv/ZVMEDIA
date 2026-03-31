from django.shortcuts import render
from users.forms import (
    UserLoginForm,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def userlogin(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Успешный вход")
            return redirect("books")
        else:
            messages.error(request, "Ошибка входа")
    else:
        form = UserLoginForm()
    return render(request, template_name="users/login.html", context={"form": form})


def userlogout(request):
    logout(request)
    return redirect("login")
