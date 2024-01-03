from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import CodeSample, Language, Note
from .forms import CheckNewCodeForm
from .serializers import NoteSerializer
from .constants import CODE_FORM_FIELD_PLACEHOLDER


def index(request: HttpRequest) -> HttpResponse:
    return redirect("/check-new-code")


def check_new_code(request: HttpRequest) -> HttpResponse:
    form = CheckNewCodeForm(
        language_choices=((lang.id, lang.name) for lang in Language.objects.all()),
    )
    result = None

    if request.method == "POST":
        form = CheckNewCodeForm(
            data=request.POST,
            language_choices=((lang.id, lang.name) for lang in Language.objects.all()),
        )
        if form.is_valid():
            if request.user.is_authenticated:
                code_sample = CodeSample(
                    code=form.cleaned_data.get("code"),
                    language_id=form.cleaned_data.get("language"),
                    result_ai=("#TODO" if form.cleaned_data.get("run_ai") else None),
                    result_static=(
                        "#TODO" if form.cleaned_data.get("run_static") else None
                    ),
                    author=request.user.username,
                    pub_date=datetime.now(),
                )
                code_sample.save()
                return redirect(f"/code-sample/{code_sample.id}")
            else:
                code_sample = CodeSample(
                    code=form.cleaned_data.get("code"),
                    language_id=form.cleaned_data.get("language"),
                    result_ai="#TODO",
                    result_static="#TODO",
                    pub_date=datetime.now(),
                )
                return render(
                    request=request,
                    template_name="checker/code_sample.html",
                    context={"code_sample": code_sample},
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
    code_samples = CodeSample.objects.filter(author=request.user.username).order_by(
        "-pub_date"
    )
    context = {"code_samples": code_samples}

    return render(
        request=request, template_name="checker/history.html", context=context
    )


class NoteApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_code_samples = CodeSample.objects.filter(
            author=request.user.username, id=request.query_params.get("code_sample")
        )
        notes = Note.objects.filter(code_sample__in=user_code_samples).order_by(
            "-pub_date"
        )
        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "code_sample": request.query_params.get("code_sample"),
            "content": request.data.get("content"),
            "pub_date": datetime.now(),
        }
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = {
            "code_sample": request.query_params.get("code_sample"),
            "content": request.data.get("content"),
            "pub_date": datetime.now(),
        }
        note = Note.objects.get(id=request.data.get("id"))
        serializer = NoteSerializer(note, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
