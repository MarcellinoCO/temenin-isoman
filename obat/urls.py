from django.urls import path

from .views import delete_obat, index, ajson, add, add_forms, edit_obat, add_from_flutter

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('forms/', add_forms, name='add_forms'),
    path('delete', delete_obat, name='delete_obat'),
    path('edit_obat', edit_obat, name='edit_obat'),
    path('json/', ajson, name = 'json'),
    path('add-from-flutter', add_from_flutter, name='add-from-flutter')
]