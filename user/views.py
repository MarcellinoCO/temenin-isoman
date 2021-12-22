from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt

from main.forms import CreateUserForm


@csrf_exempt
def sign_in(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"})

    if not request.body:
        return JsonResponse({"result": "Must provide request body!"})

    username = request.POST['username']
    password = request.POST['password']

    if not username or not password:
        return JsonResponse({"result": "Must provide username and password!"})

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "failed"})


@csrf_exempt
def sign_out(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"})

    if not request.user.is_authenticated:
        return JsonResponse({"result": "Not yet authenticated!"})

    logout(request)
    return JsonResponse({"result": "success"})


@csrf_exempt
def sign_up(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"})

    if not request.body:
        return JsonResponse({"result": "Must provide request body!"})

    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    role = request.POST['role']

    if not email or not username or not password:
        return JsonResponse({"result": "Must provide email, username, and password"})

    form = CreateUserForm({
        'username': username,
        'email': email,
        'password1': password,
        'password2': password,
    })

    if form.is_valid():
        form.save()

        user = User.objects.get(username=username)
        common_user = Group.objects.get(name="common_user")
        fasilitas_kesehatan = Group.objects.get(name="fasilitas_kesehatan")

        if role == "fasilitas_kesehatan":
            user.groups.add(fasilitas_kesehatan)
            user.is_staff = True
            user.save()
        else:
            user.groups.add(common_user)

        return JsonResponse({"result": "Sign up success!"})

    return JsonResponse({"result": "Sign up data not valid!"})


@csrf_exempt
def get_dummy(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"})

    if not request.user.is_authenticated:
        return JsonResponse({"data": "unauthorized"})

    return JsonResponse({"data": "wowowowowoww"})
