from lib2to3.pytree import Base
from re import template
from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from aplicaciones.bases.views import SinPrivilegios
from aplicaciones.facturacion.models import Cliente, FacturaEnc, FacturaDet
from aplicaciones.facturacion.forms import ClienteForm

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

class FacturaListView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "facturacion/factura_list.html"
    context_object_name="facturas"
    permission_required="facturacion.view_facturaenc"

@login_required(login_url='/login/')
@permission_required('inventario.view_facturaenc', login_url='bases:sin_privilegios')
def facturas(request, id_factura=None):
    template = "facturacion/facturas.html"

    encabezado = {
        'fecha': datetime.today()
    }
    detalle = {}
    clientes = Cliente.objects.filter(estado=True)

    contextos = {"encabezado": encabezado, "detalle": detalle, "clientes": clientes}

    return render(request, template, contextos)
