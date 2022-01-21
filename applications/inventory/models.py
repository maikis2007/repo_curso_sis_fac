from enum import unique
from django.db import models
from applications.bases.models import BasesModel
from PIL import Image
from ckeditor.fields import RichTextField

class Category(BasesModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = RichTextField(verbose_name='Descripción')
    image = models.ImageField(upload_to='inventory/categories', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return '{}'.format(self.name.upper())

    def save(self):
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        if self.image:

            image = Image.open(self.image)  # Objeto de Pillow
            width_input = image.width
            height_input = image.height

            relation = 800 / width_input
            dimentions = (800, int(height_input*relation))
            redimention_proportional = image.resize(dimentions, Image.ANTIALIAS)  # Objeto de Pillow actualizado

            image.save(self.image.path)

        super(Category, self).save()
    
    class Meta:
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"

class SubCategory(BasesModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = RichTextField(verbose_name='Descripción')
    image = models.ImageField(upload_to='inventory/subcategories', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return '{}'.format(self.name.upper())
    
    def save(self):        
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        super(SubCategory, self).save()
    
    class Meta:
        verbose_name_plural = "SubCategorías"
        verbose_name = "SubCategoría"
        unique_together = ('category', 'name')

class Mark(BasesModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = RichTextField(verbose_name='Descripción')
    image = models.ImageField(upload_to='inventory/marks', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return '{}'.format(self.name.upper())
    
    def save(self):
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        super(Mark, self).save()

    class Meta:
        verbose_name_plural = "Marcas"
        verbose_name = "Marca"

class UnitMeasure(BasesModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = RichTextField(verbose_name='Descripción')

    def __str__(self):
        return '{}'.format(self.name.upper())
    
    def save(self):
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        super(UnitMeasure, self).save()
    
    class Meta:
        verbose_name_plural = "Unidades de Medida"
        verbose_name = "Unidad de Medida"
