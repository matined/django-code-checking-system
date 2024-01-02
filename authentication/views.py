from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from random import randint

from .forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

verification_code: int = None


def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("/")


def change_password(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if not request.user.is_authenticated:
        return redirect("/auth/login")

    if request.method == "POST":
        global verification_code
        form = PasswordChangeForm(
            data=request.POST, user=request.user, verification_code=verification_code
        )
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        verification_code = randint(100000, 999999)
        send_mail(
            "Code Checker: Verification Code",
            f"Verification code: {verification_code}",
            "system@codechecker.com",
            [request.user.email],
            fail_silently=False,
        )
        form = PasswordChangeForm(
            user=request.user, verification_code=verification_code
        )

    return render(request, "authentication/change_password.html", {"form": form})
