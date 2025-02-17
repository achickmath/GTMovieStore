import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from .models import PasswordResetCode
from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from .forms import ForgotPasswordForm, ResetPasswordForm
from django.urls import reverse

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'accounts/forgot_password.html')
    elif request.method == "POST":
        email = request.POST['username']
        user = User.objects.filter(username=email).first()  # Check if user exists
        print(user)
        if user is None:
            messages.error(request, "Email not found. Please try again.")
            return redirect("accounts.forgot_password")
        else:
            return redirect(reverse("accounts.reset_password") + f"?email={email}")


def reset_password(request):
    email = request.GET.get('email')  # Retrieve email from URL

    if request.method == 'GET':
        return render(request, 'accounts/reset_password.html')

    if request.method == "POST":
        new_password = request.POST.get("new_password").strip()
        confirm_password = request.POST.get("confirm_password").strip()

        if not new_password or not confirm_password:
            messages.error(request, "Both password fields are required.")
            return render(request, 'accounts/reset_password.html', {'email': email})

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/reset_password.html', {'email': email})

        # Update user password
        user = User.objects.get(username=email)
        user.password = make_password(new_password)  # Hash password
        user.save()

        messages.success(request, "Password reset successfully! You can now log in.")
        return redirect('accounts.login')  # Redirect to login page

    return render(request, 'accounts/reset_password.html', {'email': email})