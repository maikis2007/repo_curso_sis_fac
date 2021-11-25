from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.inventario.views import *

app_name = "inventario"

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name="categorias"),
    path('categoria/new', CategoriaCreateView.as_view(), name="categoria_new"),
    path('categoria/edit/<int:pk>', CategoriaUpdateView.as_view(), name="categoria_edit"),
    path('categoria/delete/<int:pk>', CategoriaDeleteView.as_view(), name="categoria_delete"),
    path('categoria/inactivate/<int:id>', categoria_inactivate, name="categoria_inactivate"),

    path('subcategorias/', SubCategoriaListView.as_view(), name="subcategorias"),
    path('subcategoria/new', SubCategoriaCreateView.as_view(), name="subcategoria_new"),
    path('subcategoria/edit/<int:pk>', SubCategoriaUpdateView.as_view(), name="subcategoria_edit"),
    path('subcategoria/delete/<int:pk>', SubCategoriaDeleteView.as_view(), name="subcategoria_delete"),
    path('subcategoria/inactivate/<int:id>', subcategoria_inactivate, name="subcategoria_inactivate"),
]
