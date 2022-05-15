from lib2to3.pytree import Base
from re import template
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from aplicaciones.bases.views import SinPrivilegios
from aplicaciones.facturacion.models import Cliente, FacturaEnc, FacturaDet
from aplicaciones.facturacion.forms import ClienteForm
from aplicaciones.inventario.models import Producto

from datetime import datetime

# Create your views here.

class ClienteListView(SinPrivilegios, \
    generic.ListView):
    permission_required = "facturacion.view_cliente"
    model = Cliente
    template_name = "facturacion/clientes.html"
    context_object_name = "clientes"

# Refactorizacion
class VistaBaseForm(SinPrivilegios):
    context_object_name = 'cliente'
    model = Cliente
    template_name = "facturacion/cliente_form.html"
    form_class = ClienteForm

class ClienteNew(SuccessMessageMixin, VistaBaseForm, \
    generic.CreateView):
    permission_required = "facturacion.add_cliente"
    success_message = 'Cliente Creado Satisfactoriamente'
    success_url = reverse_lazy("fac:clientes")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ClienteEdit(VistaBaseForm, \
    generic.UpdateView):
    permission_required = "facturacion.change_cliente"

    # Mensaje Amarillo
    def get_success_url(self):
        messages.info(self.request, 'Cliente Editado Satisfactoriamente')
        return reverse_lazy("fac:clientes")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('facturacion.change_cliente', login_url='bases:sin_privilegios')
def cliente_estado(request, id_cliente):
    cliente = Cliente.objects.filter(pk=id_cliente).first()

    if request.method == 'POST':
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")

        return HttpResponse("ERROR")
        
    return HttpResponse("ERROR")

class ClienteDeleteView(SinPrivilegios, generic.DeleteView):
    permission_required = "facturacion.delete_cliente"
    model = Cliente
    template_name = "facturacion/cliente_delete.html"
    context_object_name = "cliente"

    def get_success_url(self):
        messages.error(self.request, 'Cliente Eliminado Satisfactoriamente')
        return reverse_lazy('fac:clientes')

class FacturaListView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "facturacion/factura_list.html"
    context_object_name="facturas"
    permission_required="facturacion.view_facturaenc"

@login_required(login_url='/login/')
@permission_required('inventario.view_facturaenc', login_url='bases:sin_privilegios')
def facturas(request, id_factura=None):
    template = "facturacion/facturas.html"

    encabezado = None
    detalle = {}

    clientes = Cliente.objects.filter(estado=True)

    if request.method == 'GET':
        enc = FacturaEnc.objects.filter(pk=id_factura).first()

        if not enc:
            encabezado = {
                'id': 0,
                'fecha': datetime.today(),
                'cliente': 0,
                'sub_total': "0.0",
                'descuento': "0.0",
                'total': "0.0"
            }
            
            detalle = None
        else:
            encabezado = {
                'id': enc.id,
                'fecha': datetime.today(),
                'cliente': enc.cliente,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            
            detalle = FacturaDet.objects.filter(factura=enc).all()

        contextos = {"encabezado": encabezado, "detalle": detalle, "clientes": clientes}
    
    elif request.method == 'POST':
        id_cliente = request.POST.get("encabezado_cliente")

        # Datos del encabezado
        fecha = request.POST.get("fecha")
        cliente = Cliente.objects.get(pk=id_cliente)

        if not id_factura:  # nueva factura
            enc = FacturaEnc(
                cliente = cliente,
                fecha = fecha
            )  # el id se genera automáticamente

            if enc:
                enc.save()
                id_factura = enc.id

        else:  # editar factura
            enc = FacturaEnc.objects.filter(pk=id_factura).first()

            if enc:  # se actualiza el cliente
                enc.cliente = cliente
                enc.save()

        if not id_factura:  # error inesperado
            messages.error(request, 'no se pudo detectar número de factura'.capitalize())
            return redirect("fac:facturas")

        # Datos del detalle
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        sub_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        producto = Producto.objects.get(codigo=codigo)  # obtencion del producto
        
        detalle = FacturaDet(
            factura = enc,
            producto = producto,
            cantidad = cantidad,
            precio = precio,
            sub_total = sub_total,
            descuento = descuento,
            total = total
        )

        if detalle:
            detalle.save()
        
        return redirect("fac:factura_edit", id_factura=id_factura)

    return render(request, template, contextos)

class ProductoFacListView(SinPrivilegios, generic.ListView):
    model = Producto
    template_name = "facturacion/buscar_producto.html"
    context_object_name = "productos"
    permission_required="inventario.view_producto"
