from django.forms import ModelForm
from .models import *


# Create QuizForm
class QuizForm(ModelForm):
    
    class Meta :
        model = AssessmentModel
        fields = "__all__"