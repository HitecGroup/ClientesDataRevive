# Generated by Django 3.1.3 on 2023-10-10 17:28

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0006_contactos_bloqueo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateField(default='2023-10-01')),
                ('IdUser', models.IntegerField()),
                ('Entidad', models.CharField(max_length=15)),
                ('IdEnt', models.CharField(max_length=80)),
                ('TipoMov', models.CharField(max_length=10)),
                ('Movimiento', models.CharField(max_length=20)),
                ('Movimientojson', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('User', models.CharField(max_length=50)),
                ('Nombre', models.CharField(max_length=100)),
                ('Pwd', models.CharField(max_length=20)),
            ],
        ),
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
