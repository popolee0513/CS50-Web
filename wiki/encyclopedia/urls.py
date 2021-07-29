from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/"+"<str:title>", views.title, name="title"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("wiki/"+"<str:title>"+"/edit", views.edit, name="edit"),
    path("search", views.search, name="search")
]
