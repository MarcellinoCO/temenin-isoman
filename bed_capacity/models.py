from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


def validate_telp(value):
    if (not value.isdigit()):
        raise ValidationError(
            _('%(value)s bukun nomor telpon yang valid'),
            params={'value': value},
        )


class Wilayah(models.Model):
    nama = models.CharField(max_length=15)

    def __str__(self):
        return self.nama


class RumahSakit(models.Model):
    nama = models.CharField(max_length=40)
    alamat = models.CharField(max_length=60)
    kapasitas = models.IntegerField()
    isi = models.IntegerField()
    telp = models.CharField(max_length=25, validators=[validate_telp])

    #kode_lokasi = models.CharField(max_length=25, null=True)
    kode_lokasi = models.ForeignKey(
        Wilayah, on_delete=models.CASCADE, null=True, default='')

    def __str__(self):
        return self.nama


class BedRequest(models.Model):
    GENDER = (('L', 'Laki-laki'), ('P', 'Perempuan'))

    rs = models.ForeignKey(RumahSakit, on_delete=models.CASCADE, null=True)
    nama = models.CharField(max_length=40)
    alamat = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, choices=GENDER, default='L')
    umur = models.IntegerField()
    telp = models.CharField(max_length=15, validators=[validate_telp])
