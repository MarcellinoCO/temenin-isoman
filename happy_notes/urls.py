from django.urls import path
from .views import index, load_notes_view, notes_json, add_from_flutter

urlpatterns = [
    path('', index, name='index'),

    path('data/', load_notes_view, name='notes-data'),
    path('notes-json', notes_json, name='notes-json'),
    path('add-from-flutter', add_from_flutter, name='add-from-flutter')
]