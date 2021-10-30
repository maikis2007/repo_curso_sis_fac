from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from aplicaciones.inventario.models import *
from aplicaciones.inventario.forms import *

class CategoriaListView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inventario/categorias.html"
    context_object_name = "categorias"
    login_url = "bases:login"

class CategoriaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inventario/categoria_form.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:categorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inventario/categoria_form.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:categorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Categoria
    template_name = "inventario/categoria_delete.html"
    context_object_name = "categoria"
    success_url = reverse_lazy("inventario:categorias")

def categoria_inactivate(request, id):
    categoria = Categoria.objects.filter(pk=id).first()

    if not categoria:
        return redirect("inventario:categorias")
    else:
        if categoria.estado:
            categoria.estado = False
        else:
            categoria.estado = True
        
        categoria.save()

        return redirect('inventario:categorias')
