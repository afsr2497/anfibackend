from django.db import models
import datetime

# Create your models here.
class usuariosAnfibio(models.Model):
    nombre = models.CharField(max_length=64,default='')
    apellido = models.CharField(max_length=64,default='')
    usuario = models.CharField(max_length=64,default='')
    email = models.CharField(max_length=64,default='')
    nroCelular = models.CharField(max_length=64,default='')
    contra = models.CharField(max_length=64,default='')
    codigoUsr = models.CharField(max_length=64,default='OP-0000')
    urlFoto = models.CharField(max_length=512,default='')

class botesAnfibio(models.Model):
    codigoBote = models.CharField(max_length=512,default='')
    urlBote = models.CharField(max_length=512,default='')

class fotosAnfibio(models.Model):
    codigoFoto = models.CharField(max_length=128,default='')
    urlFoto = models.CharField(max_length=512,default='')

class inspecctionInfo(models.Model):
    fechaInspeccion = models.CharField(max_length=128,default='')
    distancia = models.CharField(max_length=128,default='')
    duracion = models.CharField(max_length=128,default='')
    codigoBote = models.CharField(max_length=128,default='')

class inspeccionMultimediaDatos(models.Model):
    fechaInspeccion = models.CharField(max_length=128,default=datetime.datetime.now())
    distancia = models.CharField(max_length=128,default='')
    duracion = models.CharField(max_length=128,default='')
    codigoBote = models.CharField(max_length=128,default='')
    rutaFotos = models.CharField(max_length=128,default='')
    rutaVideo = models.CharField(max_length=128,default='')
    codigoInspeccion = models.CharField(max_length=128,default='')

class fotosInspeccionInformacion(models.Model):
    codigoInspeccion = models.CharField(max_length=128,default='INSP-0000,FOT-0000')
    rutaInspeccion = models.CharField(max_length=128,default='INSP-0000/')
    rutaFoto = models.CharField(max_length=128,default='')
    codigoFoto = models.CharField(max_length=128,default='')