from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProductoSerializer
from aplicaciones.inventario.models import Producto

from django.db.models import Q

# Create your views here.

class ProductoListAPIView(APIView):

    def get(self, request):
        producto = Producto.objects.all()
        data = ProductoSerializer(producto, many=True).data

        return Response(data)

class ProductoDetalle(APIView):

    def get(self, request, codigo):
        producto = get_object_or_404(Producto, Q(codigo=codigo) | Q(codigo_barra=codigo))
        data = ProductoSerializer(producto).data

        return Response(data)
