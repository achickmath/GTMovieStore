from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:movie_id>/", views.detail, name="detail"),
]