from .models import Movie
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Movie


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        latest_movie_list = Movie.objects.all()
        user = request.user
        context = {
            "latest_movie_list": latest_movie_list,
            "user": user,
        }
        # output = ", ".join([m.movie_title for m in latest_movie_list])
        return render(request, "movies/index.html", context)
    else:
        return redirect("/")

def detail(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_id)
        return render(request, "movies/detail.html", {"movie": movie})
    else:
        return redirect("/")

def landing(request):
    if (request.user.is_authenticated):
        return redirect("/home/")
    else:
        return render(request, "movies/landing.html", {})

def cart(request):
    if request.user.is_authenticated:
        return render(request, "movies/cart.html", {})
    else:
        return redirect("/")
def resetpassword_page(request):
    if request.user.is_authenticated:
        return redirect("/home/")
        # Check if the HTTP request method is POST (form submission)
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            passwordConfirm = request.POST.get('passwordConfirm')

            # Check if a user with the provided username exists
            if not User.objects.filter(username=username).exists():
                # Display an error message if the username does not exist
                messages.error(request, 'Invalid Username')
                return redirect('/resetpassword/')

            if password != passwordConfirm:
                messages.error(request, 'Passwords do not match')
                return redirect('/resetpassword/')

            user = (User.objects.get(username=username))
            user.set_password(passwordConfirm)
            user.save()

            if user is None:
                # Display an error message if authentication fails (invalid password)
                messages.error(request, "Invalid Password")
                return redirect('/login/')
            else:
                # Log in the user and redirect to the home page upon successful login
                login(request, user)
                return redirect('home')

        return render(request, "movies/resetpassword.html", {})

def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/home/')

    # Render the login page template (GET request)
    return render(request, "movies/login.html", {})

def register(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    else:
        # Check if the HTTP request method is POST (form submission)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if a user with the provided username already exists
            user = User.objects.filter(username=username)

            if user.exists():
                # Display an information message if the username is taken
                messages.info(request, "Username already taken!")
                return redirect('/register/')
            if (len(password) < 8):
                messages.info(request, 'Password is too short.')
                return redirect('/register')
            if (len(password) > 20):
                messages.info(request, "Password is too long.")
                return redirect('/register')
            uppercaseStatus = False
            specialCharacterStatus = False
            for i in range(len(password)):
                if password[i].isupper():
                    uppercaseStatus = True
                if password[i] == "!" or password[i] == "?" or password[i] == "." or password[i] == "#" or password[
                    i] == "@":
                    specialCharacterStatus = True
            if not uppercaseStatus and specialCharacterStatus:
                messages.info(request, 'The password is missing both an uppercase character and a special character.')
                return redirect('/register')
            if not uppercaseStatus:
                messages.info(request, 'Password needs at least one uppercase character.')
                return redirect('/register')
            if not specialCharacterStatus:
                messages.info(request, 'Password needs at least one special character.')
                return redirect('/register')
            # Check if a user with the provided username already exists
            user = User.objects.filter(username=username)
            if user.exists():
                # Display an information message if the username is taken
                messages.info(request, "Username already taken!")
                return redirect('/register/')
            # Create a new User object with the provided information
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            # Set the user's password and save the user object
            user.set_password(password)
            user.save()
            # Display an information message indicating successful account creation
            messages.info(request, "Account created Successfully!")
            return redirect('/login/')
            # Create a new User object with the provided information
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username
            )

            # Set the user's password and save the user object
            user.set_password(password)
            user.save()

            # Display an information message indicating successful account creation
            messages.info(request, "Account created Successfully!")
            return redirect('/login/')

        # Render the registration page template (GET request)
        return render(request, "movies/register.html", {})
def loggingout(request):
    logout(request)
    return redirect('/login/')