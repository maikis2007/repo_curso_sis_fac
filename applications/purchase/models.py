from django.db import models
from applications.bases.models import BasesModel

# Create your models here.

class Provider(BasesModel):
    description = models.CharField(max_length=100, unique=True, verbose_name='Descripción')
    addres = models.CharField(max_length=250, null=True, blank=True, verbose_name='Dirección')
    contact = models.CharField(max_length=100, verbose_name='Contacto')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono')
    email = models.EmailField(max_length=250, null=True, blank=True, verbose_name='Correo electrónico')

    def __str__(self):
        return '{}'.format(self.description.upper())

    def save(self):
        description_list = list(self.description)
        description_list[0] = description_list[0].upper()
        self.description = "".join(description_list)

        addres_list = list(self.addres)
        addres_list[0] = addres_list[0].upper()
        self.addres = "".join(addres_list)

        super(Provider, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"
        verbose_name = "Proveedor"
    