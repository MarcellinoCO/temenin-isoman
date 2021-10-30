from django.urls import path
from .views import index, load_notes_view

urlpatterns = [
    path('', index, name='index'),

    path('data/', load_notes_view, name='notes-data'),
]