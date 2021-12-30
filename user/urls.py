from django.urls import path
from .views import *


urlpatterns = [
    path('', get_user),
    path('login', sign_in),
    path('logout', sign_out),
    path('signup', sign_up),
    path('dummy', get_dummy),
]
