from re import template
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views import generic

from django.db.models import Sum

from .models import ComprasDet, ComprasEnc, Proveedor
from .forms import ProveedorForm, ComprasEncForm

from aplicaciones.bases.views import SinPrivilegios

from aplicaciones.inventario.models import Producto

import datetime

# Create your views here.

class ProveedorListView(SinPrivilegios, \
    generic.ListView):
    permission_required = "compra.view_proveedor"
    model = Proveedor
    template_name = "compra/proveedores.html"
    context_object_name = "proveedores"

class ProveedorCreateView(SuccessMessageMixin, SinPrivilegios, \
    generic.CreateView):
    permission_required = "compra.add_proveedor"
    model = Proveedor
    template_name = "compra/proveedor_form.html"
    context_object_name = "proveedor"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedores")
    success_message = "Proveedor Creado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('compra.change_proveedor', login_url='bases:sin_privilegios')
def proveedor_edit(request, id_proveedor):
    proveedor = Proveedor.objects.get(id=id_proveedor)
    template = "compra/proveedor_form.html"

    if request.method == 'GET':
        form = ProveedorForm(instance=proveedor)
    elif request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.instance.um = request.user.id
            form.save()
        messages.info(request, "Proveedor Editado Satisfactoriamente")
        return redirect("cmp:proveedores")
    
    contextos = {'form': form, 'proveedor': proveedor}
    
    return render(request, template, contextos)

class ProveedorDeleteView(SinPrivilegios, \
    generic.DeleteView):
    permission_required = "compra.delete_proveedor"
    model = Proveedor
    template_name = "compra/proveedor_delete.html"
    context_object_name = "proveedor"
    success_url = reverse_lazy("cmp:proveedores")

@login_required(login_url='bases:login')
@permission_required('compra.change_proveedor', login_url='bases:sin_privilegios')
def proveedor_estado(request, id_proveedor):
    proveedor = Proveedor.objects.filter(pk=id_proveedor).first()

    contexto = {}
    template = "compra/proveedor_estado.html"

    if not proveedor:
        return redirect("cmp:proveedores")
    else:
        if request.method == 'GET':
            contexto = {'proveedor': proveedor}

        elif request.method == 'POST':
            if proveedor.estado:
                proveedor.estado = False
            else:
                proveedor.estado = True

            proveedor.save()

            contexto = {'proveedor': 'OK'}

            if not proveedor.estado:
                return HttpResponse('Proveedor Inactivado satisfactoriamente')
            else:
                return HttpResponse('Proveedor Activado satisfactoriamente')

    return render(request, template, contexto)

class ComprasListView(SinPrivilegios, \
    generic.ListView):
    permission_required = "compra.view_comprasenc"
    model = ComprasEnc
    template_name = "compra/compras_list.html"
    context_object_name = "compras"

@login_required(login_url='bases:login')
@permission_required('compra.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request, id_compra=None):
    template = "compra/compras.html"
    productos = Producto.objects.filter(estado=True) # Filtrado de los Productos para el Detalle

    contextos = {}
    form_compra = {}

    if request.method == 'GET':
        
        form_compra = ComprasEncForm()
        encabezado = ComprasEnc.objects.filter(pk=id_compra).first() # Filtado del Encabezado

        if encabezado: # Editar
            detalle = ComprasDet.objects.filter(compra=encabezado).all() # Filtrado de los Detalles del Encabezado

            fecha_compra = datetime.date.isoformat(encabezado.fecha_compra) # Buen Formato a las Fechas
            fecha_factura = datetime.date.isoformat(encabezado.fecha_factura) # del Formulario de Encabezado

            registro = {
                'fecha_compra': fecha_compra,  #
                'proveedor': encabezado.proveedor,
                'observacion': encabezado.observacion,
                'nro_factura': encabezado.nro_factura,
                'fecha_factura': fecha_factura,  #
                'sub_total': encabezado.sub_total,
                'descuento': encabezado.descuento,
                'total': encabezado.total
            }

            form_compra = ComprasEncForm(registro) # Mostrando Datos del Encabezado

        else: # Nuevo
            if id_compra:
                return redirect("cmp:compras")
            
            detalle = None

        contextos = {'productos': productos, 'encabezado': encabezado, 'detalle': detalle, 'form_compra': form_compra}

    elif request.method == 'POST':

        """
        El formulario de Encabezado y Detalle de Compra deben de llenarse con datos válidos (son obligatorios)
        """

        # Seleccionar campos del Encabezado, mediante el id del HTML
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        nro_factura = request.POST.get("nro_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not id_compra: # Nuevo
            proveedor = Proveedor.objects.get(pk=proveedor) # Seleccionar Proveedor del Encabezado Nuevo
            # Datos del Nuevo Registro
            encabezado = ComprasEnc( # Modelo ComprasEnc
                fecha_compra = fecha_compra,
                observacion = observacion,
                nro_factura = nro_factura,
                fecha_factura = fecha_factura,
                proveedor = proveedor,
                uc = request.user
            )
            
            if encabezado:
                encabezado.save() # Guardar cambios, si los Datos están Completos

                messages.success(request, "Compra Creada Satisfactoriamente")

                id_compra = encabezado.id # Guardar el Id del Encabezado para Editar

        else: # Editar
            encabezado = ComprasEnc.objects.filter(pk=id_compra).first() # Filtrado del Encabezado

            if encabezado: # Modificación de datos
                encabezado.fecha_compra = fecha_compra
                encabezado.observacion = observacion
                encabezado.nro_factura = nro_factura
                encabezado.fecha_factura = fecha_factura
                encabezado.um = request.user.id

                encabezado.save()

                messages.info(request, "Compra Editada Satisfactoriamente")
        
        """ El detalle no puede actualizarse, por ende cuando se haga el método POST del detalle se supone que es porque se quiere crear """

        # # Seleccionar campos del Detalle, mediante el id del HTML
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle  = request.POST.get("id_descuento_detalle")
        total_detalle  = request.POST.get("id_total_detalle")

        producto = Producto.objects.get(pk=producto) # Seleccionar el Producto del Detalle Nuevo

        # Datos del nuevo registro
        detalle = ComprasDet( # Modelo ComprasDet
            compra = encabezado,
            producto = producto,
            cantidad = cantidad,
            precio_prv = precio,
            sub_total = sub_total_detalle,
            descuento = descuento_detalle,
            costo = 0,
            uc = request.user
        )

        if detalle: # Si el detalle está completo
            detalle.save() # Guardar cambios

            sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total')) # Suma todos los valores del campo sub_total del Detalle relacionado al Encabezado
            descuento = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('descuento')) # Igual para el descuento

            # Guarda esos valores para esos campos del Encabezado
            encabezado.sub_total = sub_total["sub_total__sum"]
            encabezado.descuento = descuento["descuento__sum"]

            encabezado.save() # Guarda los cambios

        # Finalizada la Acción de Nuevo o Editar Encabezado y de Crear Detalle, Redirigir a Editar
        return redirect("cmp:compra_edit", id_compra=id_compra)

    return render(request, template, contextos)

class CompraDetDeleteView(SinPrivilegios, generic.DeleteView):
    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "compra/compra_det_delete.html"
    context_object_name = "compradet"

    # Se Necesita el Id de la Compra de Encabezado para Redireccionar a Editar Compra
    def get_success_url(self):
        id_compra = self.kwargs['id_compra']
        messages.error(self.request, 'Detalle Eliminado Satisfactoriamente')  # mensaje
        return reverse_lazy('cmp:compra_edit', kwargs={'id_compra': id_compra})

@login_required(login_url='bases:login')
@permission_required('compra.change_comprasenc', login_url='bases:sin_privilegios')
def compra_estado(request, id_compra):
    compra = ComprasEnc.objects.filter(pk=id_compra).first()

    contexto = {}
    template = "compra/compra_estado.html"

    if not compra:
        return redirect('cmp:compras')
    else:
        if request.method == 'GET':
            contexto = {'compra': compra}

        elif request.method == 'POST':
            if compra.estado:
                compra.estado = False
            else:
                compra.estado = True
            
            compra.save()

            contexto = {'compra': 'OK'}

            if not compra.estado:

                messages.error(request, "Compra Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Compra Activada Satisfactoriamente")
            
            return redirect('cmp:compras')

    return render(request, template, contexto)
