from django import forms
from django.forms import widgets
from aplicaciones.inventario.models import *

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'placeholder': 'Nombre de la Categoría'
        })
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción de la Categoría'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
