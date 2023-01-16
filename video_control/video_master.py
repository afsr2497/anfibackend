"""
Script para controlar el script video_cliente.py
Se controlara dicho script a partir de senhales de linux

Autor: Alexander Francisco Segovia Razo
Empresa: Tumi Robotics
Proyectos: Robot anfibio - Robot teleoperado

"""

#Control a partir de señales:
import sys
import signal
import subprocess as sp

app_cliente = None
nombre_video = str(sys.argv[1])

def terminar_programa(signum, frame):
    print('Programa terminado')
    sys.exit()

signal.signal(signal.SIGTERM,terminar_programa)

while True:
    try:
        comandoUsuario = input('Ingrese el comando a ejecutar : ')
        if comandoUsuario == 'grabar':
            app_cliente = sp.Popen(['python3','video_cliente.py',f'{nombre_video}'])
        if comandoUsuario == 'stop':
            if app_cliente is not None:
                app_cliente.terminate()
                app_cliente = None
        if comandoUsuario == 'verificar':
            print('Comando recibido adecuadamente')
    except KeyboardInterrupt:
        print('Sistema detenido')
        sys.exit()

