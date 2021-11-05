from django import forms
from django.forms import ModelForm
from .models import *


# Create QuizForm
class QuizForm(ModelForm):
    
    class Meta :
        model = Quiz
        fields = "__all__"


