"""
import cv2
import time

#capturador = cv2.VideoCapture('http://192.168.137.80:8080/?action=stream')
capturador = cv2.VideoCapture(0)
writer = cv2.VideoWriter('ejemploAnfibio.mp4',cv2.VideoWriter_fourcc('m','p','4','v'),120,(1280,720))

#print(cv2.CAP_PROP_BUFFERSIZE)
#valor_retornado = capturador.set(cv2.CAP_PROP_BUFFERSIZE,3)
#time.sleep(1)
#print(valor_retornado)
#print(cv2.CV_CAP_PROP_BUFFERSIZE)
counter = 0
start_time = time.time()
while True:
    ret,frame = capturador.read()
    if ret:
        cv2.imshow('frame',frame)
        counter = counter + 1
    if cv2.waitKey(1) & 0xFF == 27:
        break
    end_time = time.time()
    if end_time - start_time >= 1:
        print(f'Se han visualizado {counter} frames en un segundo')
        counter = 0
        start_time = time.time()

capturador.release()
writer.release()
cv2.destroyAllWindows()
"""

import numpy as np
import cv2
from multiprocessing import Process, Queue
from multiprocessing.shared_memory import SharedMemory
import time

def produce_frames(q):
    #get the first frame to calculate size of buffer
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    shm = SharedMemory(create=True, size=frame.nbytes)
    framebuffer = np.ndarray(frame.shape, frame.dtype, buffer=shm.buf) #could also maybe use array.array instead of numpy, but I'm familiar with numpy
    framebuffer[:] = frame #in case you need to send the first frame to the main process
    q.put(shm) #send the buffer back to main
    q.put(frame.shape) #send the array details
    q.put(frame.dtype)
    try:
        while True:
            cap.read(framebuffer)
    except KeyboardInterrupt:
        pass
    finally:
        shm.close() #call this in all processes where the shm exists
        shm.unlink() #call from only one process

def consume_frames(q):
    shm = q.get() #get the shared buffer
    shape = q.get()
    dtype = q.get()
    framebuffer = np.ndarray(shape, dtype, buffer=shm.buf) #reconstruct the array
    try:
        while True:
            time.sleep(200)
            cv2.imshow("window title", framebuffer)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        pass
    finally:
        shm.close()

if __name__ == "__main__":
    q = Queue()
    producer = Process(target=produce_frames, args=(q,))
    producer.start()
    consume_frames(q)