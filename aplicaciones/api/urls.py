from django.urls import path
from .views import *

app_name = "api"

urlpatterns = [
    path('v1/productos/', ProductoListAPIView.as_view(), name="productos"),
    path('v1/productos/<str:codigo>', ProductoDetalle.as_view(), name="producto_detalle")
]
