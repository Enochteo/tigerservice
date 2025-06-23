from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validate_domain

class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_domain('gsumail.gram.edu')])
    g_number = forms.CharField(max_length=9, min_length=9, required = True)
    first_name = forms.CharField(max_length=32, required = True)
    last_name = forms.CharField(max_length = 64, required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "g_number", "email", "password1", "password2"]
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email'].help_text = "Only your @gsumail.gram.edu email is allowed"

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)