from tabnanny import verbose
from django.db import models
from aplicaciones.bases.models import BasesModel, BasesModel2
from aplicaciones.inventario.models import Producto

# Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db.models import Sum

# Create your models here.

class Cliente(BasesModel):
    NAT='Natural'
    JUD='Juridica'
    TIPO_CLIENTE = [
        (NAT, 'Natural'),
        (JUD, 'Jurídica')
    ]

    nombres = models.CharField(max_length=100)  # Dato más importante
    apellidos = models.CharField(max_length=100)  # Dato más importante
    celular = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CLIENTE, default=NAT)

    def __str__(self):
        return '{}:{}'.format(self.apellidos, self.nombres)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save()

class FacturaEnc(BasesModel2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)  # innecesaria
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)
    
    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc, self).save()

    class Meta:
        verbose_name_plural = "Encabezado de las Facturas"
        verbose_name = "Encabezado de la Factura"

class FacturaDet(BasesModel2):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles de las Facturas"
        verbose_name = "Detalle de la Factura"

#@receiver(post_save, sender=ComprasDet)