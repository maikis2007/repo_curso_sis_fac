from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.inventario.views import *

app_name = "inventario"

urlpatterns = [
    path('categorias/', categoria_list, name="categorias"),
    path('nueva/categoria/', CategoriaCreateView.as_view(), name="categoria_new"),
    path('editar/categoria/<int:pk>', CategoriaUpdateView.as_view(), name="categoria_edit"),
    path('eliminar/categoria/<int:pk>', CategoriaDeleteView.as_view(), name="categoria_delete"),
    path('cambiar/estado/categoria/<int:id>', categoria_estado, name="categoria_estado"),

    path('subcategorias/', subcategoria_list, name="subcategorias"),
    path('nueva/subcategoria/', SubCategoriaCreateView.as_view(), name="subcategoria_new"),
    path('editar/subcategoria/<int:pk>', SubCategoriaUpdateView.as_view(), name="subcategoria_edit"),
    path('eliminar/subcategoria/<int:pk>', SubCategoriaDeleteView.as_view(), name="subcategoria_delete"),
    path('cambiar/estado/subcategoria/<int:id>', subcategoria_estado, name="subcategoria_estado"),
]
