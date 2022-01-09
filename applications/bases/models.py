from django.db import models
from django.contrib.auth.models import User

# Clase base de todos los modelos

class BasesModel(models.Model):
    state = models.BooleanField(default=True, verbose_name='Estado')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Última Modificación')
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creador')
    user_updated = models.IntegerField(blank=True, null=True, verbose_name='Último Modificador')

    class Meta:
        abstract = True
