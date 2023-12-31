# Generated by Django 3.1.3 on 2023-09-25 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('IdCliente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('NombreCliente', models.CharField(max_length=50)),
                ('DireccioCliente', models.CharField(max_length=150)),
                ('ClaveExterna', models.CharField(default='0000000000', max_length=16)),
                ('TelefonoPrincipal', models.CharField(default='5555555555', max_length=12)),
                ('RFC', models.CharField(default='XAXX010101000', max_length=13)),
                ('TipoCliente', models.CharField(default='Coorporativo', max_length=50)),
                ('ClientePotencial', models.BooleanField(default=False)),
                ('Duns', models.CharField(default='ABCDEFGHIJKL-DUNS', max_length=18)),
                ('NombreAdicional', models.CharField(default='Sin Adicional', max_length=50)),
                ('Sector', models.CharField(default='Customer Service', max_length=50)),
                ('FechaNacimiento', models.DateField(default='2023-09-01')),
                ('Clasificacion', models.CharField(default='PA', max_length=15)),
                ('Estado', models.BooleanField(default=True)),
                ('Division', models.CharField(default='HAAS', max_length=60)),
                ('SucServicio', models.CharField(default='Defualt', max_length=50)),
                ('TipoEmpresa', models.CharField(default='Sin Especificar', max_length=50)),
                ('NoTurnosC', models.CharField(default='Sin Turnos', max_length=15)),
                ('NoMaqConvenC', models.CharField(default='Sin Turnos', max_length=15)),
                ('NoMaqCNC_C', models.CharField(default='Sin Turnos', max_length=15)),
                ('Tier', models.CharField(default='Sin Especificar', max_length=50)),
                ('NoMaqHT_C', models.CharField(default='Sin Turnos', max_length=15)),
                ('MatUseCHMER', models.CharField(default='Varios 2', max_length=50)),
                ('MatUseYIZUMI', models.CharField(default='Varios 2', max_length=50)),
                ('FrecuenciaCompra', models.CharField(default='Varios 2', max_length=50)),
                ('ActPriEDM', models.CharField(default='Varios 2', max_length=50)),
                ('DivisionPM', models.CharField(default='Varios 2', max_length=50)),
                ('RegionVts', models.CharField(default='Varios 2', max_length=50)),
                ('ActPriEquipo', models.CharField(default='Varios 2', max_length=50)),
                ('ActPriFAB', models.CharField(default='Varios 2', max_length=50)),
                ('MatUsoCNC_Haas', models.CharField(default='Varios 2', max_length=50)),
                ('MatUsoFab', models.CharField(default='Varios 2', max_length=50)),
                ('subDivision', models.CharField(default='Varios 2', max_length=40)),
                ('iDNielsen', models.CharField(default='Varios 2', max_length=40)),
                ('ActPriEquipoCNC', models.CharField(default='Varios 2', max_length=40)),
                ('MatViruta', models.CharField(default='Varios 2', max_length=40)),
            ],
        ),
    ]
