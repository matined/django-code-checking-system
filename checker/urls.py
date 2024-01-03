from django.urls import URLPattern, path

from . import views


urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
    path("check-new-code", views.check_new_code, name="check-new-code"),
    path("history", views.history, name="history"),
    path("code-sample/<int:id>", views.code_sample, name="code-sample"),
    path("api/v1/note", views.NoteApiView.as_view(), name="note-api"),
]
