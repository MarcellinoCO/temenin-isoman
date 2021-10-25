from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .decorators import *


# showing homepage
def home(request):
    return render(request, 'main/home.html')


# handling sign up form and create user with a spesific role (group)
def signup_user(request):
    form = CreateUserForm()

    content = {}

    # exexuted when user submit form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        role = request.POST.get('as')

        # executed when form is valid
        if form.is_valid():

            # save user and redirect user to login pages
            form.save()

            # getting user and groups object
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            common_user = Group.objects.get(name="common_user")
            fasilitas_kesehatan = Group.objects.get(name="fasilitas_kesehatan")
            print(role)
            # Aadding group
            if role == "Faskes":
                user.groups.add(fasilitas_kesehatan)
                user.is_staff = True
                user.save()
            else:
                user.groups.add(common_user)

            messages.success(request, 'Account was created for ' + username)
            return redirect('/log-in/')

        # exexuted when form is not valid
        else:

            # redirect user back to sign up page
            messages.success(request, 'Form is not valid. Try again!')
            return redirect('/sign-up/')

    # render signup.html
    content['form'] = form
    return render(request, 'main/signup.html', content)


# handling log in form and authenticate someone as a user
def login_user(request):

    # excecuted when user submiting form
    if request.method == 'POST':

        # authenticating user based on username and password
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # executed when user if valid
        if user is not None:
            login(request, user)
            return redirect('/')

        # excecuted when user is not valid
        else:
            messages.success(request, 'There was an error Loging In. Try again!')
            return redirect('/log-in/')

    # rendering login.html
    else:
        return render(request, 'main/login.html', {})


# handling log out
def logout_user(request):
    logout(request)

    # redirect to login-page
    messages.success(request, 'You Have been logged out :D')
    return redirect('/log-in/')
