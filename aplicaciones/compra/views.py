from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views import generic

from .models import Proveedor
from .forms import ProveedorForm

from aplicaciones.bases.views import SinPrivilegios

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
