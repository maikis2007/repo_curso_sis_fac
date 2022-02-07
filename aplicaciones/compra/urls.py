from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.compra.views import *

app_name = "compra"

urlpatterns = [
    path('proveedores/', ProveedorListView.as_view(), name="proveedores"),
    path('nuevo/proveedor/', ProveedorCreateView.as_view(), name="proveedor_new"),
    path('editar/proveedor/<int:id_proveedor>', proveedor_edit, name="proveedor_edit"),
    path('eliminar/proveedor/<int:pk>', ProveedorDeleteView.as_view(), name="proveedor_delete"),
    path('cambiar/estado/proveedor/<int:id_proveedor>', proveedor_estado, name="proveedor_estado"),

    path('compras/', ComprasListView.as_view(), name="compras"),
    path('nueva/compra/', compras, name="compra_new")
]