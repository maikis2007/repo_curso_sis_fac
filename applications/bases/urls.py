from django.urls import path
from django.contrib.auth import views as auth_views
from applications.bases.views import *

app_name = "bases"

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="bases/login.html"), name="login"), # Vista que inicia sesión
    path('logout/', auth_views.LogoutView.as_view(template_name="bases/login.html"), name="logout"), # Vista que cierra sesión
    path('no_privileges/', HomeNoPrivileges.as_view(), name="no_privileges")
]
