from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model =  Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'priority': forms.NumberInput(attrs={'min':1, 'max':5}), 
        }

