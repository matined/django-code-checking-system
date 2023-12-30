from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from .models import CodeSample
from .forms import CheckNewCodeForm
from .constants import CODE_FORM_FIELD_PLACEHOLDER


def index(request: HttpRequest) -> HttpResponse:
    return redirect("/check-new-code")


def check_new_code(request: HttpRequest) -> HttpResponse:
    form = CheckNewCodeForm()
    result = None

    if request.method == "POST":
        form = CheckNewCodeForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                code_sample = CodeSample(
                    code=form.cleaned_data.get("code"),
                    result_ai="#TODO",
                    result_static="#TODO",
                    author=request.user.username,
                    pub_date=datetime.now(),
                )
                code_sample.save()
                return redirect(f"/code-sample/{code_sample.id}")
            else:
                result = CodeSample(
                    code=form.cleaned_data.get("code"),
                    result_ai="#TODO",
                    result_static="#TODO",
                    author=None,
                    pub_date=None,
                )
        else:
            print(form.errors)

    context = {
        "form": form,
        "code_form_field_placeholder": CODE_FORM_FIELD_PLACEHOLDER,
        "result": result,
    }

    return render(
        request=request, template_name="checker/check_new_code.html", context=context
    )


def code_sample(request: HttpRequest, id: int) -> HttpResponse:
    code_sample = CodeSample.objects.get(id=id)
    context = {"code_sample": code_sample}

    return render(
        request=request, template_name="checker/code_sample.html", context=context
    )


def history(request: HttpRequest) -> HttpResponse:
    code_samples = CodeSample.objects.order_by("-pub_date")
    context = {"code_samples": code_samples}

    return render(
        request=request, template_name="checker/history.html", context=context
    )
