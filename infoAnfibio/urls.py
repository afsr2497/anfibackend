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
    path('capturarFotoInspeccion',views.capturarFotoInspeccion,name='capturarFotoInspeccion')
]