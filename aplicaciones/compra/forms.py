from django import forms
from django.db import models

from aplicaciones.compra.models import ComprasEnc, Proveedor

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

class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    proveedor = forms.ModelChoiceField(
        queryset = Proveedor.objects.filter(estado=True)
    )

    class Meta:
        model = ComprasEnc
        fields = ['proveedor', 'fecha_compra', 'nro_factura', 'observacion', 'fecha_factura', 'sub_total', 'descuento', \
            'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
