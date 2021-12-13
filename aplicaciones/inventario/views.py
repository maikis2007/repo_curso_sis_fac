from re import template
from typing import Generator
from django.db.models import query
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from aplicaciones.inventario.models import *
from aplicaciones.inventario.forms import *

class CategoriaListView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = "inventario/categorias/categorias.html"
    context_object_name = "categorias"
    login_url = "bases:login"

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

# Todo sucede a partir de un click en el botón de inactivar categoría
def categoria_estado(request, id): # categoria inactiva, subcategorias y productos inactivos, y viceversa
    categoria = Categoria.objects.filter(pk=id).first() # categoria a inactivar o activar

    subcategorias = SubCategoria.objects.filter(categoria=id).all() # subcategorias de la categoria

    contexto = {}
    template = "inventario/categorias/categoria_estado.html"

    if not categoria:
        return redirect('inv:categorias')
    else:
        if request.method == 'GET':
            contexto = {'categoria': categoria}
        elif request.method == 'POST':
            lista = []

            for subcategoria in subcategorias:
                id = subcategoria.pk
                lista.append(id) # lista guarda los id's de las subcategorias
            
            lista2 = []

            for id in lista:
                producto = Producto.objects.filter(subcategoria=id).all() # se obtiene los productos de cada subcategoria en un "qs"
                lista2.append(producto) # cada qs se guarda en una lista

            # Se cambia el estado al hacer click
            if categoria.estado:
                categoria.estado = False

                if subcategorias: # Para sus subcategorias
                    for subcategoria in subcategorias:
                        subcategoria.estado = False # Inactivada
                        subcategoria.save()
                if lista2: # y sus productos
                    for qs in lista2:
                        for producto in qs:
                            producto.estado = False
                            producto.save()

            else:
                categoria.estado = True

                if subcategorias:
                    for subcategoria in subcategorias:
                        subcategoria.estado = True # Activada
                        subcategoria.save()
                if lista2:
                    for qs in lista2:
                        for producto in qs:
                            producto.estado = True
                            producto.save()
                # Porque con subcategoria es uno a muchos
                # Y subcategoría hace uno a muchos con Producto

            categoria.save() # Guardar cambios, siempre

            
            contexto = {'categoria': 'OK'}

            if not categoria.estado:

                return HttpResponse('Categoría inactivada')

            else:

                return HttpResponse('Categoría activada')

    return render(request, template, contexto)

def subcategoria_list(request): # Implementación de una lógica especial en el listado de las subcategorias, permisos de usuario
    subcategorias = SubCategoria.objects.all()

    categorias = Categoria.objects.all()
    cantidad_categorias = categorias.count()

    categorias_inactivas = Categoria.objects.filter(estado=False).all()
    cantidad_categorias_inactivas = categorias_inactivas.count()

    context = {'categorias': categorias, 'cantidad_categorias': cantidad_categorias, 'cantidad_categorias_inactivas': cantidad_categorias_inactivas, 'subcategorias': subcategorias}

    template = 'inventario/subcategorias/subcategorias.html' # La lógica se observa en la plantilla

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

def subcategoria_estado(request, id): # subcategoria inactiva, productos inactivos, y viceversa
    subcategoria = SubCategoria.objects.filter(pk=id).first()

    productos_activos = Producto.objects.filter(subcategoria=id, estado=True).all()
    productos_inactivos = Producto.objects.filter(subcategoria=id, estado=False).all()

    contexto = {}

    template = "inventario/subcategorias/subcategoria_estado.html"

    if not subcategoria:
        return redirect('inv:subcategorias')
    else:
        if request.method == 'GET':
            contexto = {'subcategoria': subcategoria}
        elif request.method == 'POST':
            # Se hace la operación contraria, solo si lo necesita
            # (No voy a inactivar, el registro que ya está inactivo, XD)
            # Es otra forma, más "lógica" de hacerlo
            if subcategoria.estado:
                subcategoria.estado = False

                if productos_activos:
                    for producto in productos_activos:
                        producto.estado = False
                        producto.save()

            else:
                subcategoria.estado = True

                if productos_inactivos:
                    for producto in productos_inactivos:
                        producto.estado = True
                        producto.save()
            
            subcategoria.save()

            contexto = {'subcategoria': 'OK'}

            if not subcategoria.estado:

                return HttpResponse('Subcategoría inactivada')

            else:

                return HttpResponse('Subcategoría activada')

    return render(request, template, contexto)

class MarcaListView(LoginRequiredMixin, generic.ListView):
    model = Marca
    template_name = "inventario/marcas/marcas.html"
    context_object_name = "marcas"
    login_url = "bases:login"

class MarcaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Marca
    template_name = "inventario/marcas/marca_form.html"
    context_object_name = "marca"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marcas")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class MarcaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Marca
    template_name = "inventario/marcas/marca_form.html"
    context_object_name = "marca"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marcas")
    login_url = "bases:login"

class MarcaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Marca
    template_name = "inventario/marcas/marca_delete.html"
    context_object_name = "marca"
    success_url = reverse_lazy("inv:marcas")
    login_url = "bases:login"

def marca_estado(request, id): # marca inactiva, productos inactivos, y viceversa
    marca = Marca.objects.filter(pk=id).first()

    productos_activos = Producto.objects.filter(marca=id, estado=True).all()
    productos_inactivos = Producto.objects.filter(marca=id, estado=False).all()

    contexto = {}

    template = "inventario/marcas/marca_estado.html"
    
    if not marca:
        return redirect('inv:marcas')
    else:
        if request.method == 'GET':
            contexto = {'marca': marca}
        elif request.method == 'POST':
            if marca.estado:
                marca.estado = False

                if productos_activos:
                    for producto in productos_activos:
                        producto.estado = False
                        producto.save()

            else:
                marca.estado = True

                if productos_inactivos:
                    for producto in productos_inactivos:
                        producto.estado = True
                        producto.save()
            
            marca.save()

            contexto = {'marca': 'OK'}

            if not marca.estado:

                return HttpResponse('Marca inactivada')

            else:

                return HttpResponse('Marca activada')
    
    return render(request, template, contexto)

class UMListView(LoginRequiredMixin, generic.ListView):
    model = UnidadMedida
    template_name = "inventario/unidades_medida/um.html"
    context_object_name = "unidades"
    login_url = "bases:login"

class UMCreateView(LoginRequiredMixin, generic.CreateView):
    model = UnidadMedida
    template_name = "inventario/unidades_medida/um_form.html"
    context_object_name = "um"
    form_class = UMForm
    success_url = reverse_lazy("inv:um")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class UMUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UnidadMedida
    template_name = "inventario/unidades_medida/um_form.html"
    context_object_name = "um"
    form_class = UMForm
    success_url = reverse_lazy("inv:um")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class UMDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UnidadMedida
    template_name = "inventario/unidades_medida/um_delete.html"
    context_object_name = "um"
    success_url = reverse_lazy("inv:um")
    login_url = "bases:login"

def um_estado(request, id): # unidad de medida inactiva, productos inactivos, y viceversa
    um = UnidadMedida.objects.filter(pk=id).first()

    productos_activos = Producto.objects.filter(unidad_medida=id, estado=True).all()
    productos_inactivos = Producto.objects.filter(unidad_medida=id, estado=False).all()
    
    contexto = {}

    template = "inventario/unidades_medida/um_estado.html"

    if not um:
        return redirect('inv:um')
    else:
        if request.method == 'GET':
            contexto = {'um': um}
        elif request.method == 'POST':
            if um.estado:
                um.estado = False

                if productos_activos:
                    for producto in productos_activos:
                        producto.estado = False
                        producto.save()

            else:
                um.estado = True

                if productos_inactivos:
                    for producto in productos_inactivos:
                        producto.estado = True
                        producto.save()
            
            um.save()

            contexto = {'um': 'OK'}

            if not um.estado:

                return HttpResponse('Unidad de Medida inactivada')

            else:

                return HttpResponse('Unidad de Medida activada')

    return render(request, template, contexto)

def producto_list(request): # Implementación de una lógica más avanzada en el listado de los productos, permisos de usuario
    productos = Producto.objects.all()

    subcategorias = SubCategoria.objects.all()
    subcategorias_inactivas = SubCategoria.objects.filter(estado=False).all()

    cantidad_subcategorias = subcategorias.count()
    cantidad_subcategorias_inactivas = subcategorias_inactivas.count()

    marcas = Marca.objects.all()
    marcas_inactivas = Marca.objects.filter(estado=False).all()

    cantidad_marcas = marcas.count()
    cantidad_marcas_inactivas = marcas_inactivas.count()

    unidades_medida = UnidadMedida.objects.all()
    unidad_medida_inactivas = UnidadMedida.objects.filter(estado=False).all()

    cantidad_um = unidades_medida.count()
    cantidad_um_inactivas = unidad_medida_inactivas.count()

    context = {'subcategorias': subcategorias, 'marcas': marcas, 'unidades_medida': unidades_medida, 'cantidad_subcategorias': cantidad_subcategorias, 'cantidad_subcategorias_inactivas': cantidad_subcategorias_inactivas, 'cantidad_marcas': cantidad_marcas, 'cantidad_marcas_inactivas': cantidad_marcas_inactivas,  'cantidad_um': cantidad_um, 'cantidad_um_inactivas': cantidad_um_inactivas, 'productos': productos}

    template = 'inventario/productos/productos.html' # La lógica es similar a subcategoria_list

    return render(request, template, context)

class ProductoCreateView(LoginRequiredMixin, generic.CreateView):
    model = Producto
    template_name = "inventario/productos/producto_form.html"
    context_object_name = "producto"
    form_class = ProductoForm
    success_url = reverse_lazy("inv:productos")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ProductoUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Producto
    template_name = "inventario/productos/producto_form.html"
    context_object_name = "producto"
    form_class = ProductoForm
    success_url = reverse_lazy("inv:productos")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.producto = self.request.user.id
        return super().form_valid(form)

class ProductoDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Producto
    template_name = "inventario/productos/producto_delete.html"
    context_object_name = "producto"
    success_url = reverse_lazy("inv:productos")
    login_url = "bases:login"

def producto_estado(request, id): # producto es una tabla débil, depende de otras, por eso su inactivar es simple.
    producto = Producto.objects.filter(pk=id).first()

    contexto = {}

    template = "inventario/productos/producto_estado.html"

    if not producto:
        return redirect('inv:productos')
    else:
        if request.method == 'GET':
            contexto = {'producto': producto}
        elif request.method == 'POST':
            if producto.estado:
                producto.estado = False
            else:
                producto.estado = True
            
            producto.save()

            contexto = {'producto': 'OK'}

            if not producto.estado:

                return HttpResponse('Producto inactivado')

            else:

                return HttpResponse('Producto activado')

    return render(request, template, contexto)
