from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("show", views.show, name="show"),
    path("mylist", views.mylist, name="mylist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:title>", views.items, name="items")
]
