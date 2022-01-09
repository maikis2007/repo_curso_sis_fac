from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .models import Category, SubCategory, Mark, UnitMeasure
from .forms import CategoryForm, SubCategoryForm, MarkForm, UnitMeasureForm

from applications.bases.views import NoPrivileges

# Create your views here.

class CategoryListView(NoPrivileges, \
    ListView):
    permission_required = "inventory.view_category"
    model = Category
    template_name = "inventory/category_list.html"
    context_object_name = "obj"

class CategoryCreateView(SuccessMessageMixin, NoPrivileges, \
    CreateView):
    permission_required = "inventory.add_category"
    model = Category
    template_name = "inventory/category_form.html"
    context_object_name = "obj"
    form_class = CategoryForm
    success_url = reverse_lazy("inv:category_list")
    success_message = "Categoría Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        return super().form_valid(form)

@login_required(login_url="bases:login")
@permission_required("inventory.change_category", login_url="bases:no_privileges")
def category_edit(request, id_category):
    category = Category.objects.get(id=id_category)
    template = "inventory/category_form.html"

    if request.method == "GET":
        form = CategoryForm(instance=category)

    elif request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.instance.user_updated = request.user.id
            form.save()

        messages.info(request, "Categoría Editada Satisfactoriamente")

        return redirect("inv:category_list")
    
    contexts = {"form": form, "obj": category}
    
    return render(request, template, contexts)

@login_required(login_url="bases:login")
@permission_required("inventory.delete_category", login_url="bases:no_privileges")
def category_delete(request, id_category):
    category = Category.objects.get(id=id_category)
    template = "inventory/category_delete.html"

    if request.method == "GET":
        context = {"obj": category}

    elif request.method == "POST":
        category.delete()

        messages.error(request, "Categoría Eliminada Satisfactoriamente")

        return redirect("inv:category_list")
    
    return render(request, template, context)

@login_required(login_url="bases:login")
@permission_required("inventory.change_category", login_url="bases:no_privileges")
def category_state(request, id_category):
    category = Category.objects.filter(pk=id_category).first()
    subcategories = SubCategory.objects.filter(category=id_category).all() # Queryset

    context = {}
    template = "inventory/category_state.html"

    if not category:
        return redirect("inv:category_list")
    else:
        if request.method == "GET":
            context = {"obj": category}

        elif request.method == "POST":
            if category.state:
                category.state = False # Inactivada

                if subcategories:
                    for subcategory in subcategories:
                        subcategory.state = False # Inactivadas
                        subcategory.save()

            else:
                category.state = True # Activada

                if subcategories:
                    for subcategory in subcategories:
                        subcategory.state = True # Activadas
                        subcategory.save()

            category.save()
            
            context = {"obj": "OK"}

            if not category.state:

                messages.error(request, "Categoría Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Categoría Activada Satisfactoriamente")
            
            return redirect("inv:category_list")

    return render(request, template, context)

@login_required(login_url="bases:login")
@permission_required("inventory.view_subcategory", login_url="bases:no_privileges")
def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    categories = Category.objects.all()
    inactive_categories = Category.objects.filter(state=False).all()
    quantity_categories = categories.count()
    quantity_inactive_categories = inactive_categories.count()

    """
    if (categories): # obj2
        if (quantity_categories == quantity_inactive_categories): # obj3 and obj4
            if (subcategories): # obj
                pass
            else:
                pass
        else:
            if (subcategories):
                pass
            else:
                pass
    else:
        pass
    """

    semienlace_habilitado = '<a class="bbtn btn-primary shadow-md mr-2 inhabilitado" onclick="alert("No hay categorías");">'

    semienlace_inhabilitado = '<a class="btn btn-primary shadow-md mr-2">Nueva Categoría</a>'

    contexts = {"obj": subcategories, "obj2": categories, "obj3": quantity_categories, "obj4": quantity_inactive_categories, \
        "semienlace_habilitado": semienlace_habilitado, "semienlace_inhabilitado": semienlace_inhabilitado}

    template = "inventory/subcategory_list.html"

    return render(request, template, contexts)

class SubcategoryCreateView(SuccessMessageMixin, NoPrivileges, \
    CreateView):
    permission_required = "inventory.add_subcategory"
    model = SubCategory
    template_name = "inventory/subcategory_form.html"
    context_object_name = "obj"
    form_class = SubCategoryForm
    success_url = reverse_lazy("inv:subcategory_list")
    success_message = "SubCategoría Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url="bases:login")
@permission_required("inventory.change_subcategory", login_url="bases:no_privileges")
def subcategory_edit(request, id_subcategory):
    subcategory = SubCategory.objects.get(id=id_subcategory)
    template = "inventory/subcategory_form.html"

    if request.method == "GET":
        form = SubCategoryForm(instance=subcategory)

    elif request.method == "POST":
        form = SubCategoryForm(request.POST, instance=subcategory)

        if form.is_valid():
            form.instance.user_updated = request.user.id
            form.save()

        messages.info(request, "SubCategoría Editada Satisfactoriamente")

        return redirect("inv:subcategory_list")
    
    contexts = {"form": form, "obj": subcategory}
    
    return render(request, template, contexts)

@login_required(login_url="bases:login")
@permission_required("inventory.delete_subcategory", login_url="bases:no_privileges")
def subcategory_delete(request, id_subcategory):
    subcategory = SubCategory.objects.get(id=id_subcategory)
    template = "inventory/subcategory_delete.html"

    if request.method == "GET":
        context = {"obj": subcategory}

    elif request.method == "POST":
        subcategory.delete()

        messages.error(request, "SubCategoría Eliminada Satisfactoriamente")

        return redirect("inv:subcategory_list")
    
    return render(request, template, context)

@login_required(login_url="bases:login")
@permission_required("inventory.change_subcategory", login_url="bases:no_privileges")
def subcategory_state(request, id_subcategory): # subcategory inactiva, productos inactivos, y viceversa
    subcategory = SubCategory.objects.filter(pk=id_subcategory).first()

    context = {}
    template = "inventory/subcategory_state.html"

    if not subcategory:
        return redirect("inv:subcategory_list")
    else:
        if request.method == "GET":
            context = {"obj": subcategory}

        elif request.method == "POST":
            if subcategory.state:
                subcategory.state = False

            else:
                subcategory.state = True
            
            subcategory.save()

            context = {"obj": "OK"}

            if not subcategory.state:

                messages.error(request, "SubCategoría Inactivada Satisfactoriamente")

            else:

                messages.success(request, "SubCategoría Activada Satisfactoriamente")

            return redirect("inv:subcategory_list")

    return render(request, template, context)

class MarkListView(NoPrivileges, \
    ListView):
    permission_required = "inventory.view_mark"
    model = Mark
    template_name = "inventory/mark_list.html"
    context_object_name = "obj"

class MarkCreateView(SuccessMessageMixin, NoPrivileges, \
    CreateView):
    permission_required = "inventory.add_mark"
    model = Mark
    template_name = "inventory/mark_form.html"
    context_object_name = "obj"
    form_class = MarkForm
    success_url = reverse_lazy("inv:mark_list")
    success_message = "Marca Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url="bases:login")
@permission_required("inventory.change_mark", login_url="bases:no_privileges")
def mark_edit(request, id_mark):
    mark = Mark.objects.get(id=id_mark)
    template = "inventory/mark_form.html"

    if request.method == "GET":
        form = MarkForm(instance=mark)

    elif request.method == "POST":
        form = MarkForm(request.POST, instance=mark)

        if form.is_valid():
            form.instance.user_updated = request.user.id
            form.save()

        messages.info(request, "Marca Editada Satisfactoriamente")

        return redirect("inv:mark_list")
    
    contexts = {"form": form, "obj": mark}
    
    return render(request, template, contexts)

@login_required(login_url="bases:login")
@permission_required("inventory.delete_mark", login_url="bases:no_privileges")
def mark_delete(request, id_mark):
    mark = Mark.objects.get(id=id_mark)
    template = "inventory/mark_delete.html"

    if request.method == "GET":
        context = {"obj": mark}

    elif request.method == "POST":
        mark.delete()

        messages.error(request, "Marca Eliminada Satisfactoriamente")

        return redirect("inv:mark_list")
    
    return render(request, template, context)

@login_required(login_url="bases:login")
@permission_required("inventory.change_mark", login_url="bases:no_privileges")
def mark_state(request, id_mark):
    mark = Mark.objects.filter(pk=id_mark).first()

    context = {}
    template = "inventory/mark_state.html"
    
    if not mark:
        return redirect("inv:mark_list")
    else:
        if request.method == "GET":
            context = {"mark": mark}

        elif request.method == "POST":
            if mark.state:
                mark.state = False

            else:
                mark.state = True
            
            mark.save()

            context = {"mark": "OK"}

            if not mark.state:

                messages.error(request, "Marca Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Marca Activada Satisfactoriamente")
            
            return redirect("inv:mark_list")
    
    return render(request, template, context)

class UnitMeasureListView(NoPrivileges, \
    ListView):
    permission_required = "inventory.view_unitmeasure"
    model = UnitMeasure
    template_name = "inventory/unit_measure_list.html"
    context_object_name = "obj"

class UnitMeasureCreateView(SuccessMessageMixin, NoPrivileges, \
    CreateView):
    permission_required = "inventory.add_unitmeasure"
    model = UnitMeasure
    template_name = "inventory/unit_measure_form.html"
    context_object_name = "obj"
    form_class = UnitMeasureForm
    success_url = reverse_lazy("inv:unit_measure_list")
    success_message = "Unidad de Medida Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url="bases:login")
@permission_required("inventory.change_unitmeasure", login_url="bases:no_privileges")
def unit_measure_edit(request, id_unit_measure):
    unit_measure = UnitMeasure.objects.get(id=id_unit_measure)
    template = "inventory/unit_measure_form.html"

    if request.method == "GET":
        form = UnitMeasureForm(instance=unit_measure)

    elif request.method == "POST":
        form = UnitMeasureForm(request.POST, instance=unit_measure)

        if form.is_valid():
            form.instance.user_updated = request.user.id
            form.save()

        messages.info(request, "Unidad de Medida Editada Satisfactoriamente")

        return redirect("inv:unit_measure_list")
    
    contexts = {"form": form, "obj": unit_measure}
    
    return render(request, template, contexts)

@login_required(login_url="bases:login")
@permission_required("inventory.delete_unitmeasure", login_url="bases:no_privileges")
def unit_measure_delete(request, id_unit_measure):
    unit_measure = UnitMeasure.objects.get(id=id_unit_measure)
    template = "inventory/unit_measure_delete.html"

    if request.method == "GET":
        context = {"obj": unit_measure}

    elif request.method == "POST":
        unit_measure.delete()

        messages.error(request, "Unidad de Medida Eliminada Satisfactoriamente")

        return redirect("inv:unit_measure_list")
    
    return render(request, template, context)

@login_required(login_url="bases:login")
@permission_required("inventory.change_unitmeasure", login_url="bases:no_privileges")
def unit_measure_state(request, id_unit_measure):
    unit_measure = UnitMeasure.objects.filter(pk=id_unit_measure).first()
    
    context = {}
    template = "inventory/unit_measure_state.html"

    if not unit_measure:
        return redirect("inv:unit_measure_list")
    else:
        if request.method == "GET":
            context = {"obj": unit_measure}

        elif request.method == "POST":
            if unit_measure.state:
                unit_measure.state = False

            else:
                unit_measure.state = True
            
            unit_measure.save()

            context = {"obj": "OK"}

            if not unit_measure.state:

                messages.error(request, "Unidad de Medida Inactivada Satisfactoriamente")

            else:

                messages.success(request, "Unidad de Medida Activada Satisfactoriamente")
            
            return redirect("inv:unit_measure_list")

    return render(request, template, context)
