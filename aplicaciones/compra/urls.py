from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.compra.views import *

from .reports import reporte_compras, imprimir_compra

app_name = "compra"

urlpatterns = [
    path('proveedores/', ProveedorListView.as_view(), name="proveedores"),
    path('nuevo/proveedor/', ProveedorCreateView.as_view(), name="proveedor_new"),
    path('editar/proveedor/<int:id_proveedor>', proveedor_edit, name="proveedor_edit"),
    path('eliminar/proveedor/<int:pk>', ProveedorDeleteView.as_view(), name="proveedor_delete"),
    path('cambiar/estado/proveedor/<int:id_proveedor>', proveedor_estado, name="proveedor_estado"),

    path('compras/', ComprasListView.as_view(), name="compras"),
    path('nueva/compra/', compras, name="compra_new"),
    path('editar/compra/<int:id_compra>', compras, name="compra_edit"),
    path('compra/<int:id_compra>/eliminar/compradet/<int:pk>', CompraDetDeleteView.as_view(), name="compra_delete"),

    path('compras/listado', reporte_compras, name="compras_print"),
    path('imprimir/compra/<int:id_compra>', imprimir_compra, name="compra_print")
]
