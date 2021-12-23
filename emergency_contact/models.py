from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_telepon(value):
    if (not value.isdigit()):
        raise ValidationError(
            _('%(value)s bukan nomor telepon yang valid'),
            params={'value': value},
        )


class Daerah(models.Model):
    daerah = models.CharField(max_length=15, unique=True, default='')

    def __str__(self):
        return self.daerah

class RumahSakit(models.Model):
    nama = models.CharField(max_length=40, unique=True)
    alamat = models.CharField(max_length=60)
    telepon = models.CharField(max_length=25, validators=[validate_telepon])
    daerah = models.ForeignKey(Daerah, on_delete=models.CASCADE, null=True, default='')

    def __str__(self):
        return self.nama