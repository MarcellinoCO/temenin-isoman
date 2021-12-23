from django.urls import path
from .views import *
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', signup_user, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
