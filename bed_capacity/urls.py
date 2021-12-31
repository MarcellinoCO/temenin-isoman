from django.urls import path
from . import views

app_name = 'bed_capacity'

urlpatterns = [
    path('', views.bed_capacity, name='bed_capacity'),
    path('bed_data_json/wil/<id>', views.bed_data_json),
    path('bed_data_json/<id>', views.get_rs_data),
    path('adm', views.bed_request_admin),
    path('request_data_json', views.request_data_json),
    path('request_data_json/<id>', views.get_request_data),
    path('wilayah_json', views.wilayah_json),
]
