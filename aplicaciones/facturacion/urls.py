from django.urls import path
from django.urls.resolvers import URLPattern

from aplicaciones.facturacion.views import *

app_name = "facturacion"

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name="clientes"),
    path('nuevo/cliente/', ClienteNew.as_view(), name="cliente_new"),
    path('editar/cliente/<int:pk>', ClienteEdit.as_view(), name="cliente_edit"),
    path('estado/cliente/<int:id_cliente>', cliente_estado, name="cliente_estado"),
    path('eliminar/cliente/<int:pk>', ClienteDeleteView.as_view(), name="cliente_delete"),

    path('facturas/', FacturaListView.as_view(), name="facturas"),
    path('nueva/factura/', facturas, name="factura_new"),
    path('editar/factura/<int:id_factura>', facturas, name="factura_edit"),
    
    path('buscar/producto/', ProductoFacListView.as_view(), name="factura_producto"),
]
