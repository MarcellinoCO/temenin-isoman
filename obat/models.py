from django.db import models

# Create your models here.
class Obat(models.Model):
    penyakit = models.CharField(max_length=30)
    penjelasan= models.CharField(max_length=100)
    daftar_obat= models.CharField(max_length=100)