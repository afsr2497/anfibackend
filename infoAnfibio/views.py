from django.shortcuts import render
from django.http import JsonResponse
from .models import usuariosAnfibio,botesAnfibio, fotosAnfibio, inspecctionInfo,inspeccionMultimediaDatos
import datetime
import cv2
import os
import serial
import sys
import subprocess as sp

path_fotos_inspeccion = ''
path_videos_inspeccion = ''
video_grabacion = '0'
id_inspeccion = '0'
counter_fotos = '0'
counter_videos = '0'
frames_videos = '0'
app_video = None
#VIDEO_GRABACION es un flag que indica que el video se esta grabando

#captureVideoFoto = cv2.VideoCapture("http://localhost:8080/?action=stream")
#objSerial = serial.Serial('/dev/ttyACM0',115200)

comandosRobot = {'$OAXBTN3':'$OAX1M','$OAXBTN0':'$OAX3J0A','$OAXBTN1':'$OAX3J0B','$OAXBTN2':'$OAX3JB0'}


# Create your views here.
def infoUsuarios(request):
    usuarios_totales = usuariosAnfibio.objects.all()
    usuarios_enviar = []
    for usuario in usuarios_totales:
        usr_datos = [usuario.nombre,usuario.apellido,usuario.codigoUsr,usuario.urlFoto,usuario.usuario]
        usuarios_enviar.append(usr_datos)
    return JsonResponse({
        'usuarios':usuarios_enviar,
    })

def datosUsuario(request):
    usuario_codigo = request.GET.get('codigo')
    print(usuario_codigo)
    usuario_info = usuariosAnfibio.objects.get(codigoUsr=usuario_codigo)
    informacio_usuario = [usuario_info.nombre,usuario_info.apellido,usuario_info.usuario,usuario_info.codigoUsr,usuario_info.urlFoto]
    return JsonResponse({
        'info':informacio_usuario
    })

def crearUsuario(request):
    nombreUsr = request.GET.get('nombre')
    apelllidoUsr = request.GET.get('apellido')
    celularUsr = request.GET.get('celular')
    emailUsr = request.GET.get('email')
    contraUsr = request.GET.get('contra')
    print(nombreUsr)
    print(apelllidoUsr)
    print(celularUsr)
    print(emailUsr)
    print(contraUsr)
    usuariosAnfibio(nombre=nombreUsr,apellido=apelllidoUsr,nroCelular=celularUsr,email=emailUsr,contra=contraUsr).save()
    usr_mod = usuariosAnfibio.objects.get(nombre=nombreUsr)
    usr_mod.usuario = usr_mod.nombre.lower()
    usr_mod.save()
    codUsr = str(usr_mod.id)
    while len(codUsr) < 4:
        codUsr = '0' + codUsr
    usr_mod.codigoUsr = 'OP-' + codUsr
    usr_mod.save()
    return JsonResponse({
        'respuesta':'Ok',
    })

def accederUsuario(request):
    usrCodigo = request.GET.get('codigo')
    usrContra = request.GET.get('contra')
    print(usrCodigo)
    print(usrContra)
    usuario_acceso = usuariosAnfibio.objects.get(codigoUsr=usrCodigo)
    print(usuario_acceso.contra)
    if usrContra == usuario_acceso.contra and usuario_acceso.nombre == 'admin':
        print('Se envia la respuesta del admin')
        return JsonResponse({
            'resp':'300'
        })
    elif usrContra == usuario_acceso.contra:
        return JsonResponse({
            'resp':'200'
        })
    else:
        return JsonResponse({
            'resp':'100'
        })
    
def infoBoats(request):
    botes_totales = botesAnfibio.objects.all()
    botes_enviar = []
    for bote in botes_totales:
        arreglo_bote = [bote.codigoBote,bote.urlBote]
        botes_enviar.append(arreglo_bote)
    return JsonResponse({
        'boats':botes_enviar,
    })

def infoFotos(request):
    fotos_totales = fotosAnfibio.objects.all()
    fotos_enviar = []
    for foto in fotos_totales:
        arreglo_fotos = [foto.id,foto.codigoFoto,foto.urlFoto]
        fotos_enviar.append(arreglo_fotos)
    return JsonResponse({
        'fotos':fotos_enviar,
    })

def consultarEstadisticas(request):
    inspecciones_totales = inspeccionMultimediaDatos.objects.all()
    hora_total = 0.00
    distancia_total = 0.00
    recorridos_totales = 0
    recorridos_totales = len(inspecciones_totales)
    for inspeccion in inspecciones_totales:
        #hora_total = hora_total + round(float(inspeccion.duracion),2)
        hora_total = 25.43
    
    for inspeccion in inspecciones_totales:
        #distancia_total = distancia_total + round(float(inspeccion.distancia),2)
        distancia_total = 54.34
    
    return JsonResponse({
        'horas':str(hora_total),
        'distancia':str(distancia_total),
        'recorridos':str(recorridos_totales)
    })

def infoInspecciones(request):
    inspTotal = inspeccionMultimediaDatos.objects.all().order_by('-id')
    arreglo_enviar = []
    for inspeccion in inspTotal:
        arreglo_insp = [inspeccion.id,inspeccion.fechaInspeccion,inspeccion.distancia,inspeccion.duracion,inspeccion.codigoBote]
        arreglo_enviar.append(arreglo_insp)
    return JsonResponse({
        'inspecciones':arreglo_enviar
    })

def registrarTrabajo(request):
    global id_inspeccion
    duracionTrabajo = request.GET.get('duracion')
    distanciaTrabajo = request.GET.get('distancia')
    fechaRegistro = datetime.datetime.now().strftime('%d-%m-%Y')
    print(duracionTrabajo)
    duracionTrabajo = duracionTrabajo.split(':')
    print(duracionTrabajo)
    duracion = str(round(float(duracionTrabajo[0]) + round(float(duracionTrabajo[1])/60,2),2))
    codigoBote = 'BOT-0001'
    inspeccion_info = inspeccionMultimediaDatos.objects.get(id=id_inspeccion)
    inspeccion_info.distancia = distanciaTrabajo
    inspeccion_info.duracion = duracionTrabajo
    inspeccion_info.codigoBote = codigoBote
    inspeccion_info.save()
    inspecctionInfo(fechaInspeccion=fechaRegistro,distancia=distanciaTrabajo,duracion=duracion,codigoBote=codigoBote).save()
    return JsonResponse({
        'resp':'ok'
    })

#Colocar icono por inspeccion para poder revisar videos y fotos de inspeccion
#Roles de usuario
#Admin
#Adociar videos a inspeccion con botonos y tmb fotos
#Rol de usuario admin, operario
#Acceso de usuario Admin
# --Cerrador
#Iconos de monitoreo (saber si estan prendidos o aplicar funcion
#Guardar los datos finales e iniciales
#Lista de pruebas - App - Integracion con el robot
#Informe Final del software - 18 de Diciembre
#Puntos complementarios Agregar, pantallas, funcionalidades y variables
#Finales
#Tomar Foto - Operador - Tomar FOTO FUNCION

def foto(request,ind):
    fotoVer = fotosAnfibio.objects.get(id=ind)
    return render(request,'infoAnfibio/foto.html',{
        'fotoAnfibio':fotoVer.urlFoto,
    })

#Grabar pocision final e inicial
#Grabar la distancia total recorrida 
#Hacer las pruebas con arduino programado

def capturarFoto(request):
    ret,cv_img = captureVideoFoto.read()
    if ret:
        cv2.imwrite('FOTO_ANFIBIO.png',cv_img)
    return JsonResponse({
        'resp':'200'
    })

def fotosInspeccionTotal(request):
    fuentes_foto = []
    counter = 1
    inspecciones_totales = inspeccionMultimediaDatos.objects.all()
    for inspeccion in inspecciones_totales:
        fotos_inspeccion = os.listdir('infoAnfibio/static/' + inspeccion.rutaFotos)
        print(fotos_inspeccion)
        for foto in fotos_inspeccion:
            fuentes_foto.append([inspeccion.rutaFotos + foto,inspeccion.codigoInspeccion + '-' +foto,f'foto{counter}'])
            counter = counter + 1
    print(fuentes_foto)
    return render(request,'infoAnfibio/Album.html',{
        'fotos_totales':fuentes_foto,
        'tipo':'insp_total'
    })

def videosInpeccionEspecifico(request,ind):
    fuentes_video = []
    inspeccion_info = inspeccionMultimediaDatos.objects.get(id=ind)
    videos_inspeccion = os.listdir('infoAnfibio/static/' + inspeccion_info.rutaVideo)
    for video in videos_inspeccion:
        fuentes_video.append(inspeccion_info.codigoInspeccion + ':' + video)
    return render(request,'infoAnfibio/videoGallery.html',{
        'tipo':'insp_esp',
        'videos_totales':fuentes_video,
        'id_insp':str(ind)
    })

def videosInspeccionTotal(request):
    fuentes_video = []
    inspecciones_totales = inspeccionMultimediaDatos.objects.all()
    for inspeccion in inspecciones_totales:
        videos_inspeccion = os.listdir('infoAnfibio/static/' + inspeccion.rutaVideo)
        for video in videos_inspeccion:
            fuentes_video.append(inspeccion.codigoInspeccion + ':' +video)
    return render(request,'infoAnfibio/videoGallery.html',{
        'videos_totales':fuentes_video,
        'tipo':'insp_total'
    })

def videoPlayer(request,ind):
    print(ind)
    codigoInspeccion = ind.split(':')[0]
    nombreVideo = ind.split(':')[1]
    rutaVideo = inspeccionMultimediaDatos.objects.get(codigoInspeccion=codigoInspeccion).rutaVideo + nombreVideo
    return render(request,'infoAnfibio/videoPlayer.html',{
        'video':str(rutaVideo),
        'tipo':'insp_total',
        'id_insp':str(ind),
    })

def videoEspecifico(request,ind,info):
    codigoInspeccion = ind.split(':')[0]
    nombreVideo = ind.split(':')[1]
    id_insp = info
    rutaVideo = inspeccionMultimediaDatos.objects.get(codigoInspeccion=codigoInspeccion).rutaVideo + nombreVideo
    print(codigoInspeccion)
    print(nombreVideo)
    print(id_insp)
    return render(request,'infoAnfibio/videoPlayer.html',{
        'video':str(rutaVideo),
        'tipo':'insp_esp',
        'id_insp':str(info)
    })

def verVideos(request):
    return render(request,'infoAnfibio/video.html')

def comandoInfo(request):
    comando = request.GET.get('comando')
    #objSerial.write(comandosRobot[comando].encode())
    print(comando)
    return JsonResponse({
        'mensaje':'recibido'
    })

#y = $OAXBTN3
#X = $OAXBTN0

def iniciarInspeccion(request):
    global path_fotos_inspeccion
    global path_videos_inspeccion
    global id_inspeccion
    nueva_insp = 0
    try:
        nueva_insp = 1
        ultima_inspeccion = inspeccionMultimediaDatos.objects.latest('id')
        codigo_identificador = str(int(ultima_inspeccion.id) + 1)
        id_inspeccion = str(int(ultima_inspeccion.id) + 1)
    except:
        nueva_insp = 0
        inspeccionMultimediaDatos().save()
        ult_inspeccion = inspeccionMultimediaDatos.objects.latest('id')
        id_inspeccion = str(ult_inspeccion.id)
        codigo_identificador = str(ult_inspeccion.id)
    #CodigoInspeccion
    while(len(codigo_identificador)<4):
        codigo_identificador = '0' + codigo_identificador
    folder_videos = 'INSP-VIDEOS-' + codigo_identificador
    folder_fotos = 'INSP-FOTOS-' + codigo_identificador
    codigo_identificador = 'INSP-' + codigo_identificador

    #Ruta de fotos:
    ruta_fotos = 'fotos/' + folder_fotos + '/'

    #Ruta de videos:
    ruta_videos = 'videos/' + folder_videos + '/'

    #Codigo bote
    codigo_bote = 'BOT-0001'

    os.mkdir('./infoAnfibio/static/' + ruta_fotos)
    os.mkdir('./infoAnfibio/static/' + ruta_videos)
    path_fotos_inspeccion = './infoAnfibio/static/' + ruta_fotos
    path_videos_inspeccion = './infoAnfibio/static/' + ruta_videos
    if nueva_insp  == 1:
        inspeccionMultimediaDatos(codigoInspeccion=codigo_identificador,rutaFotos=ruta_fotos,rutaVideo=ruta_videos,codigoBote=codigo_bote).save()
    else:
        ult_inspeccion.codigoInspeccion = codigo_identificador
        ult_inspeccion.rutaFotos=ruta_fotos
        ult_inspeccion.rutaVideo=ruta_videos
        ult_inspeccion.codigoBote=codigo_bote
        ult_inspeccion.save()
        

    return JsonResponse({
        'resp':'200'
    })

def capturarFotoInspeccion(request):
    global path_fotos_inspeccion
    global counter_fotos
    nombre_foto = 'img-' + str(counter_fotos)
    counter_fotos = str(int(counter_fotos) + 1)
    capturaFotos = cv2.VideoCapture("http://192.168.137.80:8080/?action=stream")
    ret, cv_img = capturaFotos.read()
    if ret:
        cv2.imwrite(path_fotos_inspeccion + str(nombre_foto) + ".jpeg",cv_img)
        capturaFotos.release()
        return JsonResponse({
            'resp':'200'
        })
    else:
        return JsonResponse({
            'resp':'404'
        })


def detenerVideoInspeccion(request):
    global video_grabacion
    global frames_videos
    frames_videos = '0'
    video_grabacion = '0'
    return JsonResponse({
        'resp':'200'
    })

def fotosInspeccionEspecifico(request,ind):
    inspeccion_info = inspeccionMultimediaDatos.objects.get(id=ind)
    fuentes_foto = []
    counter = 1
    fotos_inspeccion = os.listdir('infoAnfibio/static/' + inspeccion_info.rutaFotos)
    print(fotos_inspeccion)
    for foto in fotos_inspeccion:
        fuentes_foto.append([inspeccion_info.rutaFotos + foto,inspeccion_info.codigoInspeccion + '-' +foto,f'foto{counter}'])
        counter = counter + 1
    print(fuentes_foto)
    return render(request,'infoAnfibio/Album.html',{
        'fotos_totales':fuentes_foto,
        'tipo':'insp_esp',
        'id_insp':str(ind),
    })

def encendeLucesFL(request):
    print('Se recepciono el comando para encender luces')
    return JsonResponse({
        'resp':'ok'
    })

def apagarLucesFL(request):
    print('Se recepciono el comando para apagar luces')
    return JsonResponse({
        'reps':'ok'
    })

def encenderLucesBL(request):
    print('Se encenderan las luces traseras')
    return JsonResponse({
        'resp':'ok'
    })

def apagarLucesBL(request):
    print('Se apagaran las luces traseras')
    return JsonResponse({
        'resp':'ok'
    })

def encenderLucesLV(request):
    print('Se encendera la hidrolavadora')
    return JsonResponse({
        'resp':'ok'
    })

def apagarLucesLV(request):
    print('Se apagara LA HIDROLAVora')
    return JsonResponse({
        'resp':'ok'
    })

def grabar_video_inspeccion_anfibio(request):
    global path_videos_inspeccion
    global counter_videos
    global app_video
    nombre_video = 'vid-' + str(counter_videos)
    counter_videos = str(int(counter_videos) + 1)
    print(f'{path_videos_inspeccion}{nombre_video}.mp4')
    app_video = sp.Popen(['python3','video_cliente.py',f'{path_videos_inspeccion}{nombre_video}.mp4'])
    return JsonResponse({
        'resp':'200',
    })

def detener_video_inspeccion_anfibio(request):
    global app_video
    if app_video is not None:
        app_video.terminate()
        app_video = None
    else:
        pass
    return JsonResponse({
        'resp':'200',
    })

