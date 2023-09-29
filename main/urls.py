from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("atc", views.atc, name="atc"),
    path("atc/<str:room>", views.room, name="room")
]
