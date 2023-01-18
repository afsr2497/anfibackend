"""
Script cliente comandado por un script maestro en la misma ubicacion
Autor: Alexander Francisco Segovia
Companhia: Tumi Robotics
Proyecto: Robot anfibio - Robot teleoperados
"""

import time
import signal
import sys
import cv2

capturador = cv2.VideoCapture('http://192.168.137.80:8080/?action=stream')
writer = cv2.VideoWriter(sys.argv[1],cv2.VideoWriter_fourcc(*"avc1"),15,(1280,720))

def terminar_programa(signum, frame):
    writer.release()
    capturador.release()
    cv2.destroyAllWindows()
    sys.exit()

signal.signal(signal.SIGTERM,terminar_programa)


counter = 0
start_time = time.time()
while True:
    ret,frame = capturador.read()
    if ret:
        writer.write(frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

"""
while True:
    print(f'Hola a estimado {sys.argv[1]}')
    time.sleep(1)
"""