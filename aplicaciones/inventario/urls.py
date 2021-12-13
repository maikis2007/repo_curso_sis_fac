from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.inventario.views import *

app_name = "inventario"

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name="categorias"),
    path('nueva/categoria/', CategoriaCreateView.as_view(), name="categoria_new"),
    path('editar/categoria/<int:pk>', CategoriaUpdateView.as_view(), name="categoria_edit"),
    path('eliminar/categoria/<int:pk>', CategoriaDeleteView.as_view(), name="categoria_delete"),
    path('cambiar/estado/categoria/<int:id>', categoria_estado, name="categoria_estado"),

    path('subcategorias/', subcategoria_list, name="subcategorias"),
    path('nueva/subcategoria/', SubCategoriaCreateView.as_view(), name="subcategoria_new"),
    path('editar/subcategoria/<int:pk>', SubCategoriaUpdateView.as_view(), name="subcategoria_edit"),
    path('eliminar/subcategoria/<int:pk>', SubCategoriaDeleteView.as_view(), name="subcategoria_delete"),
    path('cambiar/estado/subcategoria/<int:id>', subcategoria_estado, name="subcategoria_estado"),

    path('marcas/', MarcaListView.as_view(), name="marcas"),
    path('nueva/marca/', MarcaCreateView.as_view(), name="marca_new"),
    path('editar/marca/<int:pk>', MarcaUpdateView.as_view(), name="marca_edit"),
    path('eliminar/marca/<int:pk>', MarcaDeleteView.as_view(), name="marca_delete"),
    path('cambiar/estado/marca/<int:id>', marca_estado, name="marca_estado"),

    path('unidades_medida/', UMListView.as_view(), name="um"),
    path('nueva/unidad_medida/', UMCreateView.as_view(), name="um_new"),
    path('editar/unidad_medida/<int:pk>', UMUpdateView.as_view(), name="um_edit"),
    path('eliminar/unidad_medida/<int:pk>', UMDeleteView.as_view, name="um_delete"),
    path('cambiar/estado/unidad_medida/<int:id>', um_estado, name="um_estado"),

    path('productos/', producto_list, name="productos"),
    path('nuevo/producto/', ProductoCreateView.as_view(), name="producto_new"),
    path('editar/producto/<int:pk>', ProductoUpdateView.as_view(), name="producto_edit"),
    path('eliminar/producto/<int:pk>', ProductoDeleteView.as_view(), name="producto_delete"),
    path('cambiar/estado/producto/<int:id>', producto_estado, name="producto_estado"),
]
