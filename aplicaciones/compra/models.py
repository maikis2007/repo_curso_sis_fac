from django.db import models
from aplicaciones.bases.models import BasesModel
from aplicaciones.inventario.models import Producto

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db.models import Sum

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

class ComprasEnc(BasesModel):
    fecha_compra=models.DateField(null=True,blank=True)
    observacion=models.TextField(blank=True,null=True)
    nro_factura=models.CharField(max_length=100, unique=True)
    fecha_factura=models.DateField()
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self):
        if self.observacion:
            observacion_list = list(self.observacion) # Solo cambia la primera letra
            observacion_list[0] = observacion_list[0].upper()
            self.observacion = "".join(observacion_list)

        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0
            
        self.total = self.sub_total - self.descuento

        super(ComprasEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado de las Compras"
        verbose_name = "Encabezado de la Compra"

class ComprasDet(BasesModel):
    compra=models.ForeignKey(ComprasEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio_prv=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    costo=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles de las Compras"
        verbose_name="Detalle de la Compra"

@receiver(post_delete, sender=ComprasDet)
def compradet_delete(sender, instance, **kwargs):
    id_producto = instance.producto.id  # Del detalle de la compra, su producto
    id_compra = instance.compra.id  # Del detalle de la compra, su encabezado de compra

    encabezado = ComprasEnc.objects.filter(pk=id_compra).first() # El registro de compra vinculado al registro del detalle de compra

    if encabezado:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('descuento'))

        # Actualización del sub_total y el descuento y por ende el total
        encabezado.sub_total = sub_total['sub_total__sum']
        encabezado.descuento = descuento['descuento__sum']

        encabezado.save()

    producto = Producto.objects.filter(pk=id_producto).first()# El producto vinculado al registro del detalle de compra

    if producto:
        cantidadf = int(producto.existencia) - int(instance.cantidad) # existencia final = existencia - cantidad borrada
        producto.existencia = cantidadf

        producto.save()


@receiver(post_save, sender=ComprasDet)
def compradet_save(sender, instance, **kwargs):
    id_producto = instance.producto.id
    fecha_compra = instance.compra.fecha_compra

    producto = Producto.objects.filter(pk=id_producto).first()
    if producto:
        cantidadf = int(producto.existencia) + int(instance.cantidad) # existencia final = existencia inicial + cantidad agregada
        producto.existencia = cantidadf

        producto.ultima_compra = fecha_compra

        producto.save()
