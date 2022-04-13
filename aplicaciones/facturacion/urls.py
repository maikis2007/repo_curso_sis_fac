from django.urls import path
from django.urls.resolvers import URLPattern

from aplicaciones.facturacion.views import *

app_name = "facturacion"

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name="clientes"),
    path('nuevo/cliente/', ClienteNew.as_view(), name="cliente_new"),
    path('editar/cliente/<int:pk>', ClienteEdit.as_view(), name="cliente_edit"),
    path('estado/cliente/<int:id_cliente>', cliente_estado, name="cliente_estado"),

    path('facturas/', FacturaListView.as_view(), name="facturas"),
    path('nueva/factura/', facturas, name="factura_new")
]
