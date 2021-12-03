from re import template
from django.db.models import query
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from aplicaciones.inventario.models import *
from aplicaciones.inventario.forms import *

# Vista
class CategoriaListView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inventario/categorias/categorias.html"
    context_object_name = "categorias"
    login_url = "bases:login"

# Función
def categoria_list(request):
    categorias = Categoria.objects.all()

    """
    categorias_inactivas = Categoria.objects.filter(estado=False).all()

    if categorias:
        print("Hay categorias, ¿se podrán crear subcategorias?")
        if(len(categorias) == len(categorias_inactivas)):
                print("No, porque no hay categorias 'activas'")
        else:
                print("Sí, porque por lo menos una está activa")
    else:
        print("No hay categorías, no se podran crear subcategorias")
    """

    context = {'categorias': categorias}
    template = 'inventario/categorias/categorias.html'

    return render(request, template, context)

class CategoriaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = "inventario/categorias/categoria_form.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = "inventario/categorias/categoria_form.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Categoria
    template_name = "inventario/categorias/categoria_delete.html"
    context_object_name = "categoria"
    success_url = reverse_lazy("inv:categorias")

def categoria_estado(request, id):
    categoria = Categoria.objects.filter(pk=id).first()  # Categoria inactiva o activa, sus subcategorias inactivas o activas
    subcategorias_activas = SubCategoria.objects.filter(categoria=id, estado=True).all()
    subcategorias_inactivas = SubCategoria.objects.filter(categoria=id, estado=False).all()
    if not categoria:
        return redirect('inv:categorias')
    else:
        if categoria.estado:
            categoria.estado = False

            if subcategorias_activas:
                for subcategoria in subcategorias_activas:
                    subcategoria.estado = False # Inactivada
                    subcategoria.save()

        else:
            categoria.estado = True

            if subcategorias_inactivas:
                for subcategoria in subcategorias_inactivas:
                    subcategoria.estado = True # Activada
                    subcategoria.save()
        
        categoria.save()

        return redirect('inv:categorias')

# Vista
class SubCategoriaListView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "inventario/subcategorias/subcategorias.html"
    context_object_name = "subcategorias"
    login_url = "bases:login"

# Función
def subcategoria_list(request):
    subcategorias = SubCategoria.objects.all()

    categorias = Categoria.objects.all()
    cantidad_categorias = categorias.count()

    categorias_inactivas = Categoria.objects.filter(estado=False).all()
    cantidad_categorias_inactivas = categorias_inactivas.count()

    context = {'categorias': categorias, 'cantidad_categorias': cantidad_categorias, 'cantidad_categorias_inactivas': cantidad_categorias_inactivas, 'subcategorias': subcategorias}

    template = 'inventario/subcategorias/subcategorias.html'

    return render(request, template, context)

class SubCategoriaCreateView(LoginRequiredMixin, generic.CreateView):
    model = SubCategoria
    template_name = "inventario/subcategorias/subcategoria_form.html"
    context_object_name = "subcategoria"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class SubCategoriaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SubCategoria
    template_name = "inventario/subcategorias/subcategoria_form.html"
    context_object_name = "subcategoria"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategorias")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class SubCategoriaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = SubCategoria
    template_name = "inventario/subcategorias/subcategoria_delete.html"
    context_object_name = "subcategoria"
    success_url = reverse_lazy("inv:subcategorias")

def subcategoria_estado(request, id):
    """ 
        Si la categoría está activa, las subcategorías pueden estar activas o inactivas
        Si la categoría está inactiva, las subcategorías solo pueden estar inactivas
    """
    
    subcategoria = SubCategoria.objects.filter(pk=id).first()

    if subcategoria.categoria.estado:
        if not subcategoria:
            return redirect("inv:subcategorias")
        else:
            if subcategoria.estado:
                subcategoria.estado = False
            else:
                subcategoria.estado = True
            
            subcategoria.save()

            return redirect('inv:subcategorias')
