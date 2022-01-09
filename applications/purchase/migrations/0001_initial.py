# Generated by Django 2.2.25 on 2022-01-05 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Última Modificación')),
                ('user_updated', models.IntegerField(blank=True, null=True, verbose_name='Último Modificador')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Descripción')),
                ('addres', models.CharField(blank=True, max_length=250, null=True, verbose_name='Dirección')),
                ('contact', models.CharField(max_length=100, verbose_name='Contacto')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Correo electrónico')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creador')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
    ]
