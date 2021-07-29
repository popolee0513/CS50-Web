
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("following",views.following,name="following"),
    path("follow_control",views.follow_control,name="follow_control"),
    path("home/<str:user_name>",views.home,name="home"),
    path("article/<int:article_id>", views.article, name="article"),
    path("edit/<int:article_id>", views.edit, name="edit")
    
]
