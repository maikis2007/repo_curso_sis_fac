from django import forms
from django.db import models

from aplicaciones.compra.models import Proveedor

class ProveedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=250)

    class Meta:
        model = Proveedor
        fields = ['descripcion', 'contacto', 'telefono', 'direccion', 'email', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción'
        })
        self.fields['contacto'].widget.attrs.update({
            'placeholder': 'Contacto'
        })
        self.fields['telefono'].widget.attrs.update({
            'placeholder': 'Teléfono'
        })
        self.fields['direccion'].widget.attrs.update({
            'placeholder': 'Dirección'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Correo electrónico'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })