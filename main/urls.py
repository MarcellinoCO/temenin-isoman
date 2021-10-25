from django.urls import path
from .views import *
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', signup_user, name='sign-up'),
    path('log-in/', login_user, name='log-in'),
    path('log-out/', logout_user, name='log-out'),
]
