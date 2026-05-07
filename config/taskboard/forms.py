from django import forms
from .models import Task
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    recipients = forms.CharField(required=False, help_text='Comma seperated emails')

    class Meta:
        model =  Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'recipients']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'priority': forms.NumberInput(attrs={'min':1, 'max':5}), 
        }
    
    def clean_recipients(self):
        raw = self.cleaned_data.get('recipients', '').strip()
        if not raw:
            return []
        
        emails = [e.strip() for e in raw.split(',') if e.strip()]
        for e in emails:
            try:
                validate_email(e)
            except ValidationError:
                raise ValidationError(f"Invalid email: {e}")

        return emails