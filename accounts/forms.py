from django import forms
from django.contrib.auth.models import User
from .validators import validate_unique_emial


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField(label='Login', required=True)
    email = forms.EmailField(required=True, validators=[validate_unique_emial])
    password = forms.CharField(label='Haslo', min_length=6, max_length=20, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']




