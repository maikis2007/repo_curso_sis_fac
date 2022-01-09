from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic import ListView, CreateView, DeleteView

from .models import Provider
from .forms import ProviderForm

from applications.bases.views import NoPrivileges

# Create your views here.

class ProviderListView(NoPrivileges, \
    ListView):
    permission_required = "purchase.view_provider"
    model = Provider
    template_name = "purchase/provider_list.html"
    context_object_name = "obj"

class ProviderCreateView(SuccessMessageMixin, NoPrivileges, \
    CreateView):
    permission_required = "purchase.add_provider"
    model = Provider
    template_name = "purchase/provider_form.html"
    context_object_name = "obj"
    form_class = ProviderForm
    success_url = reverse_lazy("cmp:provider_list")
    success_message = "Proveedor Creado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        return super().form_valid(form)

@login_required(login_url="bases:login")
@permission_required("purchase.change_provider", login_url=reverse_lazy("bases:no_privileges"))
def provider_edit(request, id_provider):
    provider = Provider.objects.get(id=id_provider)
    template = "purchase/provider_form.html"

    if request.method == "GET":
        form = ProviderForm(instance=provider)

    elif request.method == "POST":
        form = ProviderForm(request.POST, instance=provider)

        if form.is_valid():
            form.instance.user_updated = request.user.id
            form.save()

        messages.info(request, "Proveedor Editado Satisfactoriamente")

        return redirect("cmp:provider_list")
    
    contextos = {"form": form, "provider": provider}
    
    return render(request, template, contextos)

class ProviderDeleteView(NoPrivileges, \
    DeleteView):
    permission_required = "purchase.delete_provider"
    model = Provider
    template_name = "purchase/provider_delete.html"
    context_object_name = "obj"
    success_url = reverse_lazy("cmp:provider_list")

@login_required(login_url="bases:login")
@permission_required("purchase.change_provider", login_url=reverse_lazy("bases:no_privileges"))
def provider_state(request, id_provider):
    provider = Provider.objects.filter(pk=id_provider).first()

    contexto = {}
    template = "purchase/provider_state.html"

    if not provider:
        return redirect("cmp:provider_list")
    else:
        if request.method == "GET":
            contexto = {"provider": provider}

        elif request.method == "POST":
            if provider.state:
                provider.state = False

            else:
                provider.state = True

            provider.save()

            contexto = {"provider": "OK"}

            if not provider.state:
                return HttpResponse("Proveedor Inactivado Satisfactoriamente")
            else:
                return HttpResponse("Proveedor Activado Satisfactoriamente")

    return render(request, template, contexto)
