from django import forms
from .models import Obat

class ObatForm (forms.ModelForm):
    class Meta:
        model = Obat
        fields = "__all__"