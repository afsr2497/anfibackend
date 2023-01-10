# Generated by Django 4.1.4 on 2022-12-22 19:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infoAnfibio', '0006_inspecctioninfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='inspeccionMultimediaDatos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInspeccion', models.CharField(default=datetime.datetime(2022, 12, 22, 19, 48, 31, 666442), max_length=128)),
                ('distancia', models.CharField(default='', max_length=128)),
                ('duracion', models.CharField(default='', max_length=128)),
                ('codigoBote', models.CharField(default='', max_length=128)),
                ('rutaFotos', models.CharField(default='', max_length=128)),
                ('rutaVideo', models.CharField(default='', max_length=128)),
            ],
        ),
    ]
