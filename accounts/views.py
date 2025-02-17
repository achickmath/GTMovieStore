import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
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

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            code = generate_verification_code()
            PasswordResetCode.objects.create(user=user, code=code, created_at=now())
            send_mail(
                "Password Reset Code",
                f"Your verification code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session["reset_email"] = email
            return redirect("verify_code")
        else:
            messages.error(request, "Email not found.")
    return render(request, "accounts/forgot_password.html")

def verify_code(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        code = request.POST.get("code")
        user = User.objects.filter(email=email).first()
        if user:
            reset_entry = PasswordResetCode.objects.filter(user=user, code=code).first()
            if reset_entry:
                request.session["verified_email"] = email
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid code.")
    return render(request, "accounts/verify_code.html")

def resetpassword(request):
    if request.method == "POST":
        email = request.session.get("verified_email")
        new_password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if user:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. You can log in now.")
            return redirect("login")
    return render(request, "accounts/resetpassword.html")