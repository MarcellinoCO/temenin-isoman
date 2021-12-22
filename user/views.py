from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt

from main.forms import CreateUserForm


@csrf_exempt
def sign_in(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"}, status=405)

    if not request.body:
        return JsonResponse({"result": "Must provide request body!"}, status=400)

    username = request.POST['username']
    password = request.POST['password']

    if not username or not password:
        return JsonResponse({"result": "Must provide username and password!"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"result": "success"}, status=200)
    else:
        return JsonResponse({"result": "failed"}, status=500)


@csrf_exempt
def sign_out(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"result": "Not yet authenticated!"}, status=403)

    logout(request)
    return JsonResponse({"result": "success"}, status=200)


@csrf_exempt
def sign_up(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"}, status=405)

    if not request.body:
        return JsonResponse({"result": "Must provide request body!"}, status=400)

    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    role = request.POST['role']

    if not email or not username or not password:
        return JsonResponse({"result": "Must provide email, username, and password"}, status=400)

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

        return JsonResponse({"result": "Sign up success!"}, status=200)

    return JsonResponse({"result": "Sign up data not valid!"}, status=400)


@csrf_exempt
def get_dummy(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"result": "Not yet authenticated!"}, status=403)

    return JsonResponse({"data": "wowowowowoww"}, status=200)


@csrf_exempt
def get_user(request):
    if request.method != "POST":
        return JsonResponse({"result": "Must use POST method!"}, status=405)

    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"result": "Not yet authenticated!"}, status=403)

    user = User.objects.get(username=user)
    roles = list(user.groups.values_list('name', flat=True))

    return JsonResponse({"data": {"username": user.username, "email": user.email, "roles": roles}}, status=200)
