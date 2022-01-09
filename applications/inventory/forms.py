from django import forms
from django.forms import widgets
from applications.inventory.models import *

# Estructura y presentación de los formularios

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'state']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descripción de la Categoría'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SubCategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset = Category.objects.filter(state=True)
    )

    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'description', 'image', 'state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descripción de la SubCategoría'
        })
        self.fields['category'].empty_label = "Seleccione la Categoría"
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['name', 'description', 'image', 'state']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descripción de la Marca'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class UnitMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitMeasure
        fields = ['name', 'description', 'state']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Descripción de la Unidad de Medida'
        })
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
