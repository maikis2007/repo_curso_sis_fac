from django.urls import path
from django.urls.resolvers import URLPattern
from aplicaciones.compra.views import *

app_name = "compra"

urlpatterns = [
    path('proveedores/', ProveedorListView.as_view(), name="proveedores"),
    path('nuevo/proveedor/', ProveedorCreateView.as_view(), name="proveedor_new"),
    path('editar/proveedor/<int:pk>', ProveedorUpdateView.as_view(), name="proveedor_edit"),
    path('eliminar/proveedor/<int:pk>', ProveedorDeleteView.as_view(), name="proveedor_delete"),
    path('cambiar/estado/proveedor/<int:id>', proveedor_estado, name="proveedor_estado"),
]
