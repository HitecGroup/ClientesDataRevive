# Generated by Django 3.1.3 on 2023-10-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0004_country_region_relreg_edo_sepomex'),
    ]

    operations = [
        migrations.AddField(
            model_name='direcciones',
            name='Bloqueo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='direcciones',
            name='DireccionUUID',
            field=models.CharField(default='000000000000', max_length=32),
        ),
        migrations.AlterField(
            model_name='direcciones',
            name='Ciudad',
            field=models.CharField(default='Sin Dato', max_length=80),
        ),
        migrations.AlterField(
            model_name='direcciones',
            name='Distrito',
            field=models.CharField(default='Sin Dato', max_length=50),
        ),
    ]
