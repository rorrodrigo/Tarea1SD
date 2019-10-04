import socket
import os.path
import sys
import struct
from _thread import *
import threading

IP_HOST_D = '0.0.0.0'
PORT = 5000


socket_d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_d.bind((IP_HOST_D,PORT))
socket_d.listen (10)

mutex = threading.Lock()

def Main(s,addr):
    while True:
        mensaje = s.recv(1024)
        if not mensaje:
            s.close()
            break

        mensaje = mensaje.decode('utf-8').strip()

        if(mensaje == "Cerrar_Servidor"):
            print("Cerrando Servidor")
            s.close()
            break
            
        mutex.acquire()
        archivo_data = open("data.txt","a")
        archivo_data.write("Mensaje: " + mensaje + "\n")
        print(mensaje)
        archivo_data.close()
        mutex.release()

        s.send("ACK".encode('utf-8'))

def responder_multicast():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 10000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, address = sock.recvfrom(1024)
        if(data.decode('utf-8') == "status?"):
            sock.sendto('1'.encode(), address)

start_new_thread(responder_multicast, ())

while True:
    connection, client_address = socket_d.accept()
    print('connection from', client_address)
    start_new_thread(Main, (connection, client_address,))
