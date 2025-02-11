from django.urls import path
from django.contrib import admin  # Django admin module
from django.urls import path       # URL routing
from django.conf import settings   # Application settings
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_page, name="login"),
    path('register/', views.register, name='register'),
    path('login/resetpassword/', views.resetpassword_page, name='register'),
    path("home/", views.home, name="home"),
    path("home/<int:movie_id>/", views.detail, name="detail"),
    path("loggingout/", views.loggingout,name="loggingout"),
    path("cart/", views.cart, name="cart"),
]