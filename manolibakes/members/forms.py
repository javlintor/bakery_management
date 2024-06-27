from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LogInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Introduzca nombre de usuario",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Introduzca contraseña",
            }
        )
    )
