from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'image']  # Add event_date here

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 150px;', 'placeholder': 'Event Description'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Add this
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
