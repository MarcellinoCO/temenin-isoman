from .models import Note
from django import forms

class NoteForm(forms.ModelForm):
    sender = forms.CharField(widget=forms.TextInput())
    title = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}))
    class Meta:
        model = Note
        fields = ('sender', 'title', 'message')