from django.db import models
from applications.bases.models import BasesModel

class Category(BasesModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(help_text='Descripción de la Categoría', unique=True, verbose_name='Descripción')
    image = models.ImageField(upload_to="inventario/categorias", height_field=800, width_field=800, null=True, blank=True, \
        verbose_name='Imagen')

    def __str__(self):
        return '{}'.format(self.name.upper())

    def save(self):
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        super(Category, self).save()
    
    class Meta:
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"

class SubCategory(BasesModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(help_text='Descripción de la SubCategoría', verbose_name='Descripción')
    image = models.ImageField(upload_to='inventario/subcategorias', height_field=800, width_field=800, null=True, blank=True, \
        verbose_name='Imagen')

    def __str__(self):
        return '{}:{}'.format(self.nombre.upper())
    
    def save(self):        
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        super(SubCategory, self).save()
    
    class Meta:
        verbose_name_plural = "SubCategorías"
        verbose_name = "SubCategoría"
        unique_together = [('category', 'description'), ('category', 'name')]

class Mark(BasesModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(help_text='Descripción de la Marca', unique=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='inventario/marcas', height_field=800, width_field=800, null=True, blank=True, verbose_name='Imagen')

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
    description = models.TextField(help_text='Descripción de la Marca', unique=True, verbose_name='Descripción')

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
