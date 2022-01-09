from django import forms
from django.db import models

from applications.purchase.models import Provider

class ProviderForm(forms.ModelForm):
    email = forms.EmailField(max_length=250)

    class Meta:
        model = Provider
        fields = ['description', 'contact', 'phone', 'addres', 'email', 'state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descripción'
        })
        self.fields['contact'].widget.attrs.update({
            'placeholder': 'Contacto'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Teléfono'
        })
        self.fields['addres'].widget.attrs.update({
            'placeholder': 'Dirección'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Correo electrónico'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })