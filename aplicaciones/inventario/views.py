from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.api import success
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UMForm, ProductoForm

from aplicaciones.bases.views import SinPrivilegios

# Create your views here.

class CategoriaListView(SinPrivilegios, \
    ListView):
    permission_required = "inventario.view_categoria"
    model = Categoria
    template_name = "inventario/categorias.html"
    context_object_name = "categorias"

class CategoriaCreateView(SuccessMessageMixin, SinPrivilegios, \
    CreateView):
    permission_required = "inventario.add_categoria"
    model = Categoria
    template_name = "inventario/categoria_form.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categorias")
    success_message = "Categoría Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('inventario.change_categoria', login_url='bases:sin_privilegios')
def categoria_edit(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    template = "inventario/categoria_form.html"

    if request.method == 'GET':
        form = CategoriaForm(instance=categoria)

    elif request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)

        if form.is_valid():
            form.instance.um = request.user.id
            form.save()

        messages.info(request, "Categoría Editada Satisfactoriamente") # Por esta línea, es una función

        return redirect("inv:categorias")
    
    contextos = {'form': form, 'categoria': categoria}
    
    return render(request, template, contextos)

@login_required(login_url='bases:login')
@permission_required('inventario.delete_categoria', login_url='bases:sin_privilegios')
def categoria_delete(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    template = "inventario/categoria_delete.html"

    if request.method == 'GET':
        contexto = {'categoria': categoria}

    elif request.method == 'POST':
        categoria.delete()

        messages.error(request, "Categoría Eliminada Satisfactoriamente") # Por esta línea, es una función

        return redirect("inv:categorias")
    
    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.change_categoria', login_url='bases:sin_privilegios')
def categoria_estado(request, id_categoria): # Categoría inactivas, subcategorias y productos también, y viceversa
    categoria = Categoria.objects.filter(pk=id_categoria).first()
    subcategorias = SubCategoria.objects.filter(categoria=id_categoria).all() # Queryset

    contexto = {}
    template = "inventario/categoria_estado.html"

    if not categoria:
        return redirect('inv:categorias')
    else:
        if request.method == 'GET':
            contexto = {'categoria': categoria}

        elif request.method == 'POST':
            id_subcategorias = []

            for subcategoria in subcategorias:
                id_subcategoria = subcategoria.pk
                id_subcategorias.append(id_subcategoria)
            
            productos = []

            for id_subcategoria in id_subcategorias:
                producto = Producto.objects.filter(subcategoria=id_subcategoria).all() # Queryset, tiene registros
                productos.append(producto) # Lista de Querysets

            if categoria.estado:
                categoria.estado = False # Inactivada

                if subcategorias:
                    for subcategoria in subcategorias:
                        subcategoria.estado = False # Inactivada
                        subcategoria.save()

                if productos: # y sus productos
                    for qs in productos:
                        for producto in qs:
                            producto.estado = False # Inactivada
                            producto.save()

            else:
                categoria.estado = True # Activada

                if subcategorias:
                    for subcategoria in subcategorias:
                        subcategoria.estado = True # Activada
                        subcategoria.save()

                if productos:
                    for qs in productos:
                        for producto in qs:
                            producto.estado = True # Activada
                            producto.save()

            categoria.save() # Cambios realizados
            
            contexto = {'categoria': 'OK'}

            """Ya no se hará una operación reversa"""
            if not categoria.estado:

                messages.error(request, "Categoría Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Categoría Activada Satisfactoriamente")
            
            return redirect("inv:categorias")

    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.view_subcategoria', login_url='bases:sin_privilegios')
def subcategoria_list(request):
    subcategorias = SubCategoria.objects.all()
    categorias = Categoria.objects.all()
    categorias_inactivas = Categoria.objects.filter(estado=False).all()

    cantidad_categorias = categorias.count()
    cantidad_categorias_inactivas = categorias_inactivas.count()

    contextos = {'categorias': categorias, 'subcategorias': subcategorias, 'cantidad_categorias': cantidad_categorias, 'cantidad_categorias_inactivas': cantidad_categorias_inactivas}

    template = 'inventario/subcategorias.html' # La lógica se observa en la plantilla

    return render(request, template, contextos)

class SubCategoriaCreateView(SuccessMessageMixin, SinPrivilegios, \
    CreateView):
    permission_required = "inventario.add_subcategoria"
    model = SubCategoria
    template_name = "inventario/subcategoria_form.html"
    context_object_name = "subcategoria"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategorias")
    success_message = "SubCategoría Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('inventario.change_subcategoria', login_url='bases:sin_privilegios')
def subcategoria_edit(request, id_subcategoria):
    subcategoria = SubCategoria.objects.get(id=id_subcategoria)
    template = "inventario/subcategoria_form.html"

    if request.method == 'GET':
        form = SubCategoriaForm(instance=subcategoria)

    elif request.method == 'POST':
        form = SubCategoriaForm(request.POST, instance=subcategoria)

        if form.is_valid():
            form.instance.um = request.user.id
            form.save()

        messages.info(request, "SubCategoría Editada Satisfactoriamente")

        return redirect("inv:subcategorias")
    
    contextos = {'form': form, 'subcategoria': subcategoria}
    
    return render(request, template, contextos)

@login_required(login_url='bases:login')
@permission_required('inventario.delete_subcategoria', login_url='bases:sin_privilegios')
def subcategoria_delete(request, id_subcategoria):
    subcategoria = SubCategoria.objects.get(id=id_subcategoria)
    template = "inventario/subcategoria_delete.html"

    if request.method == 'GET':
        contexto = {'subcategoria': subcategoria}

    elif request.method == 'POST':
        subcategoria.delete()

        messages.error(request, "SubCategoría Eliminada Satisfactoriamente")

        return redirect("inv:subcategorias")
    
    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.change_subcategoria', login_url='bases:sin_privilegios')
def subcategoria_estado(request, id_subcategoria): # subcategoria inactiva, productos inactivos, y viceversa
    subcategoria = SubCategoria.objects.filter(pk=id_subcategoria).first()
    productos = Producto.objects.filter(subcategoria=id_subcategoria).all()

    contexto = {}
    template = "inventario/subcategoria_estado.html"

    if not subcategoria:
        return redirect('inv:subcategorias')
    else:
        if request.method == 'GET':
            contexto = {'subcategoria': subcategoria}

        elif request.method == 'POST':

            if subcategoria.estado:
                subcategoria.estado = False

                if productos:
                    for producto in productos:
                        producto.estado = False
                        producto.save()

            else:
                subcategoria.estado = True

                if productos:
                    for producto in productos:
                        producto.estado = True
                        producto.save()
            
            subcategoria.save()

            contexto = {'subcategoria': 'OK'}

            if not subcategoria.estado:

                messages.error(request, "SubCategoría Inactivada Satisfactoriamente")

            else:

                messages.success(request, "SubCategoría Activada Satisfactoriamente")

            return redirect("inv:subcategorias")

    return render(request, template, contexto)

class MarcaListView(SinPrivilegios, \
    ListView):
    permission_required = "inventario.view_marca"
    model = Marca
    template_name = "inventario/marcas.html"
    context_object_name = "marcas"

class MarcaCreateView(SuccessMessageMixin, SinPrivilegios, \
    CreateView):
    permission_required = "inventario.add_marca"
    model = Marca
    template_name = "inventario/marca_form.html"
    context_object_name = "marca"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marcas")
    success_message = "Marca Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('inventario.change_marca', login_url='bases:sin_privilegios')
def marca_edit(request, id_marca):
    marca = Marca.objects.get(id=id_marca)
    template = "inventario/marca_form.html"

    if request.method == 'GET':
        form = MarcaForm(instance=marca)

    elif request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)

        if form.is_valid():
            form.instance.um = request.user.id
            form.save()

        messages.info(request, "Marca Editada Satisfactoriamente")

        return redirect("inv:marcas")
    
    contextos = {'form': form, 'marca': marca}
    
    return render(request, template, contextos)

@login_required(login_url='bases:login')
@permission_required('inventario.delete_marca', login_url='bases:sin_privilegios')
def marca_delete(request, id_marca):
    marca = Marca.objects.get(id=id_marca)
    template = "inventario/marca_delete.html"

    if request.method == 'GET':
        contexto = {'marca': marca}

    elif request.method == 'POST':
        marca.delete()

        messages.error(request, "Marca Eliminada Satisfactoriamente")

        return redirect("inv:marcas")
    
    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.change_marca', login_url='bases:sin_privilegios')
def marca_estado(request, id_marca):
    marca = Marca.objects.filter(pk=id_marca).first()

    productos = Producto.objects.filter(marca=id_marca).all()

    contexto = {}
    template = "inventario/marca_estado.html"
    
    if not marca:
        return redirect('inv:marcas')
    else:
        if request.method == 'GET':
            contexto = {'marca': marca}

        elif request.method == 'POST':
            if marca.estado:
                marca.estado = False

                if productos:
                    for producto in productos:
                        producto.estado = False
                        producto.save()

            else:
                marca.estado = True

                if productos:
                    for producto in productos:
                        producto.estado = True
                        producto.save()
            
            marca.save()

            contexto = {'marca': 'OK'}

            if not marca.estado:

                messages.error(request, "Marca Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Marca Activada Satisfactoriamente")
            
            return redirect("inv:marcas")
    
    return render(request, template, contexto)

class UMListView(SinPrivilegios, \
    ListView):
    permission_required = "inventario.view_unidadmedida"
    model = UnidadMedida
    template_name = "inventario/um.html"
    context_object_name = "unidades"

class UMCreateView(SuccessMessageMixin, SinPrivilegios, \
    CreateView):
    permission_required = "inventario.add_unidadmedida"
    model = UnidadMedida
    template_name = "inventario/um_form.html"
    context_object_name = "um"
    form_class = UMForm
    success_url = reverse_lazy("inv:um")
    success_message = "Unidad de Medida Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('inventario.change_unidadmedida', login_url='bases:sin_privilegios')
def um_edit(request, id_um):
    um = UnidadMedida.objects.get(id=id_um)
    template = "inventario/um_form.html"

    if request.method == 'GET':
        form = UMForm(instance=um)

    elif request.method == 'POST':
        form = UMForm(request.POST, instance=um)

        if form.is_valid():
            form.instance.um = request.user.id
            form.save()

        messages.info(request, "Unidad de Medida Editada Satisfactoriamente")

        return redirect("inv:um")
    
    contextos = {'form': form, 'um': um}
    
    return render(request, template, contextos)

@login_required(login_url='bases:login')
@permission_required('inventario.delete_unidadmedida', login_url='bases:sin_privilegios')
def um_delete(request, id_um):
    um = UnidadMedida.objects.get(id=id_um)
    template = "inventario/um_delete.html"

    if request.method == 'GET':
        contexto = {'um': um}

    elif request.method == 'POST':
        um.delete()

        messages.error(request, "Unidad de Medida Eliminada Satisfactoriamente")

        return redirect("inv:um")
    
    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.change_unidadmedida', login_url='bases:sin_privilegios')
def um_estado(request, id_um):
    um = UnidadMedida.objects.filter(pk=id_um).first()

    productos = Producto.objects.filter(unidad_medida=id_um).all()
    
    contexto = {}
    template = "inventario/um_estado.html"

    if not um:
        return redirect('inv:um')
    else:
        if request.method == 'GET':
            contexto = {'um': um}

        elif request.method == 'POST':
            if um.estado:
                um.estado = False

                if productos:
                    for producto in productos:
                        producto.estado = False
                        producto.save()

            else:
                um.estado = True

                if productos:
                    for producto in productos:
                        producto.estado = True
                        producto.save()
            
            um.save()

            contexto = {'um': 'OK'}

            if not um.estado:

                messages.error(request, "Unidad de Medida Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Unidad de Medida Activada Satisfactoriamente")
            
            return redirect("inv:um")

    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.view_producto', login_url='bases:sin_privilegios')
def producto_list(request):
    productos = Producto.objects.all()
    subcategorias = SubCategoria.objects.all()
    marcas = Marca.objects.all()
    unidades_medida = UnidadMedida.objects.all()

    subcategorias_inactivas = SubCategoria.objects.filter(estado=False).all()
    marcas_inactivas = Marca.objects.filter(estado=False).all()
    unidad_medida_inactivas = UnidadMedida.objects.filter(estado=False).all()

    cantidad_subcategorias = subcategorias.count()
    cantidad_marcas = marcas.count()
    cantidad_um = unidades_medida.count()

    cantidad_subcategorias_inactivas = subcategorias_inactivas.count()
    cantidad_marcas_inactivas = marcas_inactivas.count()
    cantidad_um_inactivas = unidad_medida_inactivas.count()

    contextos = {'productos': productos, 'subcategorias': subcategorias, 'marcas': marcas, 'unidades_medida': unidades_medida, 'cantidad_subcategorias': cantidad_subcategorias, \
        'cantidad_marcas': cantidad_marcas, 'cantidad_um': cantidad_um, 'cantidad_subcategorias_inactivas': cantidad_subcategorias_inactivas, 'cantidad_marcas_inactivas': cantidad_marcas_inactivas, \
            'cantidad_um_inactivas': cantidad_um_inactivas}

    template = 'inventario/productos.html' # La lógica es similar a subcategoria_list

    return render(request, template, contextos)

class ProductoCreateView(SuccessMessageMixin, SinPrivilegios, \
    CreateView):
    permission_required = "inventario.add_producto"
    model = Producto
    template_name = "inventario/producto_form.html"
    context_object_name = "producto"
    form_class = ProductoForm
    success_url = reverse_lazy("inv:productos")
    success_message = "Producto Creado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url='bases:login')
@permission_required('inventario.change_producto', login_url='bases:sin_privilegios')
def producto_edit(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    template = "inventario/producto_form.html"

    if request.method == 'GET':
        form = ProductoForm(instance=producto)

    elif request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.instance.um = request.user.id
            form.save()

        messages.info(request, "Producto Editado Satisfactoriamente")

        return redirect("inv:productos")
    
    contextos = {'form': form, 'producto': producto}
    
    return render(request, template, contextos)

@login_required(login_url='bases:login')
@permission_required('inventario.delete_producto', login_url='bases:sin_privilegios')
def producto_delete(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    template = "inventario/producto_delete.html"

    if request.method == 'GET':
        contexto = {'producto': producto}

    elif request.method == 'POST':

        producto.delete()

        messages.error(request, "Producto Eliminado Satisfactoriamente")

        return redirect("inv:productos")
    
    return render(request, template, contexto)

@login_required(login_url='bases:login')
@permission_required('inventario.change_producto', login_url='bases:sin_privilegios')
def producto_estado(request, id_producto):
    producto = Producto.objects.filter(pk=id_producto).first()

    contexto = {}
    template = "inventario/producto_estado.html"

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

                messages.error(request, "Producto Inactivado Satisfactoriamente")

            else:

                messages.success(request, "Producto Activado Satisfactoriamente")
            
            return redirect("inv:productos")

    return render(request, template, contexto)
