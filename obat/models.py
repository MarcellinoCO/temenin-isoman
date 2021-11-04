from django.db import models

# Create your models here.
class Obat(models.Model):
    penyakit = models.CharField(max_length=100)
    penjelasan= models.CharField(max_length=1000)
    daftar_obat= models.CharField(max_length=1000)