from django.forms import ModelForm
from django import forms
from .models import Customer


class CustomerForm(ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    lastname = forms.CharField(label="Apellidos", max_length=100)

    class Meta:
        model = Customer
        fields = ['name', 'lastname']
