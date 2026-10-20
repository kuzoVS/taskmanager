from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("archive/", views.archive, name="archive"),
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/<int:pk>/delete/", views.delete_note, name="delete_note"),
    path("notes/<int:pk>/pin/", views.toggle_pin, name="toggle_pin"),
    path("notes/<int:pk>/archive/", views.toggle_archive, name="toggle_archive"),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
