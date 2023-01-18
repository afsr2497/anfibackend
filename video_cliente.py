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

capturador = cv2.VideoCapture('/dev/video0')
writer = cv2.VideoWriter(sys.argv[1],cv2.VideoWriter_fourcc('m','p','4','v'),30,(1280,720))

def terminar_programa(signum, frame):
    capturador.release()
    writer.release()
    cv2.destroyAllWindows()
    sys.exit()

signal.signal(signal.SIGTERM,terminar_programa)


counter = 0
start_time = time.time()
while True:
    ret,frame = capturador.read()
    if ret:
        writer.write(frame)
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

"""
while True:
    print(f'Hola a estimado {sys.argv[1]}')
    time.sleep(1)
"""