from django.contrib import admin
from .models import Wilayah, RumahSakit, BedRequest

# Register your models here.
admin.site.register(Wilayah)
admin.site.register(RumahSakit)
admin.site.register(BedRequest)
