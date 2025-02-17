from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_code/", views.verify_code, name="verify_code"),
    path("resetpassword/", views.resetpassword, name="resetpassword"),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
]