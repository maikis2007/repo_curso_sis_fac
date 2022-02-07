from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.inventario.views import *

app_name = "inventario"

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name="categorias"),
    path('nueva/categoria/', CategoriaCreateView.as_view(), name="categoria_new"),
    path('editar/categoria/<int:id_categoria>', categoria_edit, name="categoria_edit"),
    path('eliminar/categoria/<int:id_categoria>', categoria_delete, name="categoria_delete"),
    path('cambiar/estado/categoria/<int:id_categoria>', categoria_estado, name="categoria_estado"),

    path('subcategorias/', subcategoria_list, name="subcategorias"),
    path('nueva/subcategoria/', SubCategoriaCreateView.as_view(), name="subcategoria_new"),
    path('editar/subcategoria/<int:id_subcategoria>', subcategoria_edit, name="subcategoria_edit"),
    path('eliminar/subcategoria/<int:id_subcategoria>', subcategoria_delete, name="subcategoria_delete"),
    path('cambiar/estado/subcategoria/<int:id_subcategoria>', subcategoria_estado, name="subcategoria_estado"),

    path('marcas/', MarcaListView.as_view(), name="marcas"),
    path('nueva/marca/', MarcaCreateView.as_view(), name="marca_new"),
    path('editar/marca/<int:id_marca>', marca_edit, name="marca_edit"),
    path('eliminar/marca/<int:id_marca>', marca_delete, name="marca_delete"),
    path('cambiar/estado/marca/<int:id_marca>', marca_estado, name="marca_estado"),

    path('unidades_medida/', UMListView.as_view(), name="um"),
    path('nueva/unidad_medida/', UMCreateView.as_view(), name="um_new"),
    path('editar/unidad_medida/<int:id_um>', um_edit, name="um_edit"),
    path('eliminar/unidad_medida/<int:id_um>', um_delete, name="um_delete"),
    path('cambiar/estado/unidad_medida/<int:id_um>', um_estado, name="um_estado"),

    path('productos/', producto_list, name="productos"),
    path('nuevo/producto/', ProductoCreateView.as_view(), name="producto_new"),
    path('editar/producto/<int:id_producto>', producto_edit, name="producto_edit"),
    path('eliminar/producto/<int:id_producto>', producto_delete, name="producto_delete"),
    path('cambiar/estado/producto/<int:id_producto>', producto_estado, name="producto_estado")
]
