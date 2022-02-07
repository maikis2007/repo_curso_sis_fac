from django.db import models
from aplicaciones.bases.models import BasesModel
from aplicaciones.inventario.models import Producto

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
        verbose_name = "Proveedor"

class ComprasEnc(BasesModel):
    fecha_compra=models.DateField(null=True,blank=True)
    observacion=models.TextField(blank=True,null=True)
    no_factura=models.CharField(max_length=100)
    fecha_factura=models.DateField()
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self):
        self.observacion = self.observacion.upper()
        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0
            
        self.total = self.sub_total - self.descuento
        super(ComprasEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado de las Compras"
        verbose_name="Encabezado de la Compra"

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
        self.sub_total = float(self.cantidad) * self.precio_prv
        self.total = self.sub_total - self.descuento
        super(ComprasDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles de las Compras"
        verbose_name="Detalle de la Compra"
