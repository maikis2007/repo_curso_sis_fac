from re import template
from django.db.models import query
from django.http import response
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from aplicaciones.compra.models import *
from aplicaciones.compra.forms import *

# Create your views here.

class ProveedorListView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "compra/proveedores/proveedores.html"
    context_object_name = "proveedores"
    login_url = "bases:login"

class ProveedorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Proveedor
    template_name = "compra/proveedores/proveedor_form.html"
    context_object_name = "proveedor"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedores")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ProveedorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Proveedor
    template_name = "compra/proveedores/proveedor_form.html"
    context_object_name = "proveedor"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedores")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class ProveedorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Proveedor
    template_name = "compra/proveedores/proveedor_delete.html"
    context_object_name = "proveedor"
    success_url = reverse_lazy("cmp:proveedores")
    login_url = "bases:login"

def proveedor_estado(request, id):
    proveedor = Proveedor.objects.filter(pk=id).first()
    contexto = {}
    template = "compra/proveedores/proveedor_estado.html"

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
                return HttpResponse('Proveedor inactivado')
            else:
                return HttpResponse('Proveedor activado')

    return render(request, template, contexto)
