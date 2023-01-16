from . import views
from django.urls import path

app_name='infoAnfibio'

urlpatterns = [
    path('infoUsuarios',views.infoUsuarios,name='infoUsuarios'),
    path('crearUsuario',views.crearUsuario,name='crearUsuario'),
    path('accederUsuario',views.accederUsuario,name='accederUsuario'),
    path('datosUsuario',views.datosUsuario,name='datosUsuario'),
    path('infoBoats',views.infoBoats,name='infoBoats'),
    path('infoFotos',views.infoFotos,name='infoFotos'),
    path('consultarEstadisticas',views.consultarEstadisticas,name='consultarEstadisticas'),
    path('infoInspecciones',views.infoInspecciones,name='infoInspecciones'),
    path('registrarTrabajo',views.registrarTrabajo,name='registrarTrabajo'),
    path('foto/<str:ind>',views.foto,name='foto'),
    path('capturarFoto',views.capturarFoto,name='capturarFoto'),
    path('fotosInspeccionTotal',views.fotosInspeccionTotal,name='fotosInspeccionTotal'),
    path('verVideos',views.verVideos,name='verVideos'),
    path('comandoInfo',views.comandoInfo,name='comandoInfo'),
    path('iniciarInspeccion',views.iniciarInspeccion,name='iniciarInspeccion'),
    path('capturarFotoInspeccion',views.capturarFotoInspeccion,name='capturarFotoInspeccion'),
    path('fotosInspeccionEspecifico/<str:ind>',views.fotosInspeccionEspecifico,name='fotosInspeccionEspecifico'),
    path('encenderLucesFL',views.encendeLucesFL,name='encenderLucesFL'),
    path('apagarLucesFL',views.apagarLucesFL,name='apagarLucesFL'),
    path('encenderLucesBL',views.encenderLucesBL,name='encenderLucesBL'),
    path('apagarLucesBL',views.apagarLucesBL,name='apagarLucesBL'),
    path('encenderLucesLV',views.encenderLucesLV,name='encenderLucesLV'),
    path('apagarLucesLV',views.apagarLucesLV,name='apagarLucesLV'),
    path('grabar_video_inspeccion_anfibio',views.grabar_video_inspeccion_anfibio,name='grabar_video_inspeccion_anfibio'),
    path('detener_video_inspeccion_anfibio',views.detener_video_inspeccion_anfibio,name='detener_video_inspeccion_anfibio'),
]