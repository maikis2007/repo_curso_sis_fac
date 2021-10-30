from django.urls import path
from django.contrib.auth import views as auth_views
from aplicaciones.bases.views import HomeView

app_name = "bases"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="bases/login.html"), name="login"), # Vista que inicia sesión
    path('logout/', auth_views.LogoutView.as_view(template_name="bases/login.html"), name="logout"), # Vista que cierra sesión
]
