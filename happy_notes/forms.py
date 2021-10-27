from .models import Note
from django import forms

class NoteForm(forms.ModelForm):
    sender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}))
    class Meta:
        model = Note
        fields = ('sender', 'title', 'message')