from django.contrib import admin
from aplicaciones.inventario.models import *

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Marca)
admin.site.register(UnidadMedida)
admin.site.register(Producto)