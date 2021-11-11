from django.urls import path
from .views import *


urlpatterns = [
    path('', checklist_home),
    path('start', start_quarantine),
    path('quarantine-data', get_quarantine_data)
]
