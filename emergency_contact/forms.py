from django import forms
from .models import RumahSakit, Daerah

class DaerahForm(forms.ModelForm):
    class Meta:
        model = Daerah
        fields = ["daerah"]
    widgets = {
        'daerah': forms.IntegerField(widget=forms.TextInput()),
    }

class RumahSakitForm(forms.ModelForm):
    class Meta:
        model = RumahSakit
        fields = ['nama', 'alamat', 'telepon', 'daerah']
    widgets = {
        'nama': forms.CharField(widget=forms.TextInput()),
        'alamat': forms.CharField(widget=forms.TextInput()),
        'telepon': forms.IntegerField(widget=forms.TextInput()),
        'daerah': forms.IntegerField(widget=forms.TextInput()),
        }
