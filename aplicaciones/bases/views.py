from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser

from django.views.generic import TemplateView

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = "bases:login"
    raise_exception = False

    def handle_no_permission(self): # Sin Permisos

        if not self.request.user == AnonymousUser(): # Logeado
            self.login_url = "bases:sin_privilegios" # Plantilla

            return HttpResponseRedirect(reverse_lazy(self.login_url)) # Muestrala
        else:
            return super().handle_no_permission()

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "bases/home.html"
    login_url = "bases:login"

class HomeSinPrivilegios(TemplateView):
    template_name = "bases/sin_privilegios.html"
