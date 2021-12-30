from tips_and_tricks.models import TipsAndTrick
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'
    

class AddForm(forms.ModelForm):
    class Meta:
        model = TipsAndTrick
        fields = '__all__'
        widgets = {
            'published_date': DateInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['type'] = 'text'
