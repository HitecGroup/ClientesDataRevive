# Generated by Django 3.1.3 on 2023-10-17 21:14

from django.db import migrations, models


class Migration(migrations.Migration):


    operations = [
        migrations.AddField(
            model_name='clientes',
            name='DivCNC',
            field=models.CharField(default='000', max_length=3),
        ),
        migrations.AddField(
            model_name='clientes',
            name='DivHTools',
            field=models.CharField(default='000', max_length=3),
        ),
        migrations.AddField(
            model_name='clientes',
            name='DivHaas',
            field=models.CharField(default='000', max_length=3),
        ),
        migrations.AddField(
            model_name='clientes',
            name='DivNextec',
            field=models.CharField(default='000', max_length=3),
        ),
        migrations.AddField(
            model_name='clientes',
            name='DivPM',
            field=models.CharField(default='000', max_length=3),
        )
    ]
