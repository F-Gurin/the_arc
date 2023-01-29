from django import forms

from .models import Sessions


class SessionsForm(forms.ModelForm):
    class Meta:
        model = Sessions
        fields = ['date_time', 'session_type', 'language']
        help_text = {
            'date_time': 'Session start date and time',
            'session_type': 'Session type',
            'language': 'Session language',
        }
        widgets = {
            'date_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%d-%m-%YT%H:%M',
            ),
            'session_type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'language': forms.Select(
                attrs={
                    'class': 'form-control'}
            ),
        }
