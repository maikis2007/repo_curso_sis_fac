from django import forms
from django.forms import widgets
from aplicaciones.inventario.models import *

# Estructura y presentación de los formularios

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        fields = ['categoria', 'descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción de la SubCategoría'
        })
        self.fields['categoria'].empty_label = "Seleccione la Categoría"
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['descripcion', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción de la Marca'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class UMForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['descripcion', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción de la Unidad de Medida'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'codigo_barra', 'descripcion', 'estado', 'precio', 'existencia', 'ultima_compra', 'marca', 'subcategoria', 'unidad_medida']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs.update({
            'placeholder': 'Código de Control Interno'
        })
        self.fields['codigo_barra'].widget.attrs.update({
            'placeholder': 'Código de Barra del Producto'
        })
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción del Producto'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['existencia'].widget.attrs['readonly'] = True
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
