from django.db import models
from aplicaciones.bases.models import BasesModel

# Create your models here.

class Proveedor(BasesModel):
    descripcion = models.CharField(max_length=100, unique=True) # primera mayúscula
    direccion = models.CharField(max_length=250, null=True, blank=True) # primera mayúscula
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion.upper())

    def save(self):
        descripcion_list = list(self.descripcion) # Solo cambia la primera letra
        descripcion_list[0] = descripcion_list[0].upper()
        self.descripcion = "".join(descripcion_list)

        direccion_list = list(self.direccion) # Solo cambia la primera letra
        direccion_list[0] = direccion_list[0].upper()
        self.direccion = "".join(direccion_list)

        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"
        verbose_name = "Proveedores"
    