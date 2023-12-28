from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import CodeSample


def index(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="base.html")


def check_new_code(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="check_new_code.html")


def history(request: HttpRequest) -> HttpResponse:
    code_samples = CodeSample.objects.order_by("-pub_date")
    context = {"code_samples": code_samples}

    return render(request=request, template_name="history.html", context=context)


def profile(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="profile.html")
