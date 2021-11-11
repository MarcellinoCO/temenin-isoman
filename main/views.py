from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import serializers

from .forms import CreateUserForm
from .decorators import *


# Show home page.
def home(request):
    return render(request, 'home.html')


# Handle sign up form and create User with a spesific role (group).
def signup_user(request):
    form = CreateUserForm()
    content = {}

    # Executed when User submit the form.
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        role = request.POST.get('as')

        # Executed when form is valid.
        if form.is_valid():
            # Save User and redirect User to login pages.
            form.save()

            # Get User and Groups object
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            common_user = Group.objects.get(name="common_user")
            fasilitas_kesehatan = Group.objects.get(name="fasilitas_kesehatan")

            # Add coresponding group.
            if role == "Faskes":
                user.groups.add(fasilitas_kesehatan)
                user.is_staff = True
                user.save()
            else:
                user.groups.add(common_user)

            messages.success(request, 'Account was created for ' + username)
            return redirect('/login/')

        # Executed when form is not valid. Redirect User back to signup page.
        else:
            messages.success(request, 'Form is not valid. Try again!')
            return redirect('/signup/')

    # Render signup.html.
    content['form'] = form
    return render(request, 'signup.html', content)


# Handling login form and authenticate someone as a User.
def login_user(request):
    # Excecuted when User submit the form.
    if request.method == 'POST':
        # Authenticate User based on username and password.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Executed when User is valid. Redirect to home page.
        if user is not None:
            login(request, user)
            return redirect('/')

        # Executed when User is not valid. Redirect to login page.
        else:
            messages.success(request, 'There was an error Loging In. Try again!')
            return redirect('/login/')

    # Rendering login.html.
    else:
        return render(request, 'login.html', {})


# Handle User log out.
def logout_user(request):
    logout(request)

    # Redirect to home page.
    messages.success(request, 'You Have been logged out :D')
    return redirect('/')