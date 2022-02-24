import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .models import ComprasEnc, ComprasDet
from django.utils import timezone

def link_callback(uri, rel):
    """
     Convierta los URI HTML en rutas absolutas del sistema para que xhtml2pdf pueda acceder a esos
     recursos
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/
            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri
    # asegúrese de que ese archivo existe
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def reporte_compras(request):
    template = 'compra/compras_print.html'
    today = timezone.now()

    compras = ComprasEnc.objects.all()
    contextos = {'compras': compras, 'today': today, 'request': request}

    # Cree un objeto de respuesta de Django y especifique content_type como pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="compras_print.pdf"'
    
    # encuentra la plantilla y renderízala.
    template = get_template(template)
    html = template.render(contextos)

    # crear un pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    
    # si hay un error, muestra una vista divertida
    if pisa_status.err:
       return HttpResponse('Nosotros tuvimos algunos errores <pre>' + html + '</pre>')

    return response

def imprimir_compra(request, id_compra):
    template = "compra/compra_print.html"
    today = timezone.now()

    encabezado = ComprasEnc.objects.filter(id=id_compra).first()
    if encabezado:
        detalle = ComprasDet.objects.filter(compra=id_compra)
    else:
        detalle = None
        
    contextos = {
       'encabezado': encabezado,
       'detalle': detalle,
       'today': today,
       'request': request
    }
    
    # Cree un objeto de respuesta de Django y especifique content_type como pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="compra_print.pdf"'  # attachment
    
    # encuentra la plantilla y renderízala.
    template = get_template(template)
    html = template.render(contextos)

    # crear un pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    
    # si hay un error, muestra una vista divertida
    if pisa_status.err:
       return HttpResponse('Nosotros tuvimos algunos errores <pre>' + html + '</pre>')

    return response
