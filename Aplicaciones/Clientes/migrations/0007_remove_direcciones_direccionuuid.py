# Generated by Django 3.1.3 on 2023-09-27 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0006_direcciones_direccionuuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direcciones',
            name='DireccionUUID',
        ),
    ]