from enum import unique
from django.db import models
from django.db.models.constraints import UniqueConstraint
from aplicaciones.bases.models import BasesModel

class Categoria(BasesModel):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()

        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(Categoria, self).save()
    
    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categorias"

class SubCategoria(BasesModel):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '{}:{}'.format(self.nombre, self.categoria.nombre)
    
    def save(self):
        self.nombre = self.nombre.upper()

        descripcion_list = list(self.descripcion)
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        super(SubCategoria, self).save()
    
    class Meta:
        verbose_name_plural = "SubCategorias"
        verbose_name = "SubCategorias"
        unique_together = [('categoria', 'nombre'), ('categoria', 'descripcion')]
