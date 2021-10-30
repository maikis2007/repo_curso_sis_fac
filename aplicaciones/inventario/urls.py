from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.inventario.views import *

app_name = "inventario"

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name="categorias"),
    path('categorias/new', CategoriaCreateView.as_view(), name="categoria_new"),
    path('categorias/edit/<int:pk>', CategoriaUpdateView.as_view(), name="categoria_edit"),
    path('categorias/delete/<int:pk>', CategoriaDeleteView.as_view(), name="categoria_delete"),
    path('categorias/inactivate/<int:id>', categoria_inactivate, name="categoria_inactivate")
]
