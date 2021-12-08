from enum import unique
from django.db import models
from django.db.models.constraints import UniqueConstraint
from aplicaciones.bases.models import BasesModel

class Categoria(BasesModel):
    nombre = models.CharField(max_length=50, help_text='Nombre de la Categoría', unique=True)
    descripcion = models.CharField(max_length=250, help_text='Descripción de la Categoría', unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        nombre_list = list(self.nombre) # Solo cambia la primera letra
        nombre_list[0] = nombre_list[0].upper()
        self.nombre = "".join(nombre_list)

        descripcion_list = list(self.descripcion) # Solo cambia la primera letra
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(Categoria, self).save()
    
    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categorias"

class SubCategoria(BasesModel):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, help_text='Nombre de la SubCategoría')
    descripcion = models.CharField(max_length=250, help_text='Descripción de la SubCategoría')

    def __str__(self):
        return '{}:{}'.format(self.nombre, self.categoria.nombre)
    
    def save(self):
        nombre_list = list(self.nombre)
        nombre_list[0] = nombre_list[0].upper()
        self.nombre = "".join(nombre_list)
        
        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(SubCategoria, self).save()
    
    class Meta:
        verbose_name_plural = "SubCategorias"
        verbose_name = "SubCategorias"
        unique_together = [('categoria', 'nombre'), ('categoria', 'descripcion')]

class Marca(BasesModel):
    nombre = models.CharField(max_length=50, help_text='Nombre de la Marca', unique=True)
    descripcion = models.CharField(max_length=250, help_text='Descripción de la Marca', unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)
    
    def save(self):
        nombre_list = list(self.nombre)
        nombre_list[0] = nombre_list[0].upper()
        self.nombre = "".join(nombre_list)

        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(Marca, self).save()

    class Meta:
        verbose_name_plural = "Marcas"
        verbose_name = "Marcas"

class UnidadMedida(BasesModel):
    nombre = models.CharField(max_length=50, help_text='Nombre de la Unidad de Medida', unique=True)
    descripcion = models.CharField(max_length=250, help_text='Descripción de la Unidad de Medida', unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)
    
    def save(self):
        nombre_list = list(self.nombre)
        nombre_list[0] = nombre_list[0].upper()
        self.nombre = "".join(nombre_list)

        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(UnidadMedida, self).save()
    
    class Meta:
        verbose_name_plural = "Unidades de Medida"
        verbose_name = "Unidades de Medida"

class Producto(BasesModel):
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)

    codigo = models.CharField(max_length=20, unique=True)
    codigo_barra = models.CharField(max_length=50)

    descripcion = models.CharField(max_length=350)

    precioc = models.FloatField(default=0)
    preciov = models.FloatField(default=0)

    existencia = models.IntegerField(default=0)
    ultima_compra = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(Producto, self).save()
    
    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Productos"
        unique_together = ('codigo', 'codigo_barra')
