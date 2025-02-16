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
    path("home/cart/", views.cart, name="cart"),
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
]