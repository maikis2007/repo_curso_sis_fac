from django import forms
from django.forms import widgets
from aplicaciones.inventario.models import *

# Estructura y presentación de los formularios

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

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.filter(estado=True)
    )

    class Meta:
        model = SubCategoria
        fields = ['categoria', 'nombre', 'descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'placeholder': 'Nombre de la SubCategoría'
        })
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción de la SubCategoría'
        })
        self.fields['categoria'].empty_label = "Seleccione la Categoría"
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
