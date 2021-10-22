from django.urls import path
from .views import index, json, add

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('json/', json, name = 'json'),
]