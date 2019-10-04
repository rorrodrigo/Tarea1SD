import socket
import time
import sys
import struct
import threading
from _thread import *

#Config del socket
IP_HOST_D = '0.0.0.0'
PORT = 5000

#Se crea el socket datanode-server y se espera hastas que se conecte el servidor
socket_d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_d.bind((IP_HOST_D,PORT))
socket_d.listen (5)

#Se crea un mutex que se utilizara para que no ocurran errores
mutex = threading.Lock()

### Definicion de la funcion main del datanode
def Main(s,addr):
    while True:
        #Se espera por el mensaje del server
        mensaje = s.recv(1024)
        #Si no hay mensaje se cierra el socket
        if not mensaje:
            s.close()
            break
        #Se decodifica el mensaje y se escribe en el archivo
        mensaje = mensaje.decode()
        mutex.acquire()
        archivo_data = open("data.txt","a")
        archivo_data.write("Mensaje: " + mensaje + "\n")
        print("Mensaje '",mensaje,"' guardado con exito en datanode 2")
        archivo_data.close()
        mutex.release()
        #Se envia el mensaje de respuesta al server de que escribio correctamente el mensaje
        s.send("ACK".encode())

### Definicion de la funcion que responde a los mensajes multicast del servidor
def responder_multicast():
    #Config del socket multicast
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    #Se espera por el mensaje y luego se responde con el numero del datanode
    while True:
        data, address = sock.recvfrom(1024)
        if(data.decode() == "status?"):
            sock.sendto('2'.encode(), address)

## Se crea el thread para el recibo y envio de mensajes multicast
start_new_thread(responder_multicast, ())

## Se crea el while para las conexiones que realiza el server cada vez que quiere guardar un mensaje del cliente
while True:
    datanode, address = socket_d.accept()
    start_new_thread(Main, (datanode, address,))
