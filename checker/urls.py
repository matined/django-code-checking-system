from django.urls import URLPattern, path

from . import views


urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
    path("check-new-code", views.check_new_code, name="check-new-code"),
    path("history", views.history, name="history"),
    path("profile", views.profile, name="profile"),
]
