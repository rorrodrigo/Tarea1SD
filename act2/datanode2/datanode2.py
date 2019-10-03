import socket
import os.path

import sys
import struct

# def responder_multicast():
#
#     MCAST_GRP = '224.1.1.1'
#     MCAST_PORT = 5007
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
#     # to MCAST_GRP, not all groups on MCAST_PORT
#     mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#
#     sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#
#     # Receive/respond loop
#     while True:
#         print('waiting to receive message')
#         data, address = sock.recvfrom(1024)
#
#         print('received {} bytes from {}'.format(
#             len(data), address))
#         print(data)
#
#         if(data.decode() == "status"):
#             sock.sendto('2'.encode(), address)
#         elif(data.decode()) == "shutdown":
#             sock.sendto('ack'.encode(), address)

host = '0.0.0.0'
puerto = 5002

#Creación socket (lado datanode)
obj = socket.socket()
#Conexión con el servidor.
obj.connect((host, puerto))

try:
    reg = "data.txt"
    if (os.path.isfile(reg)):
        archivo = open(reg, "a")
    else:
        archivo = open(reg, "w")

#crear un thread que ejecute la funcion responder_multicast()
finally:
    while True:
        mensaje = obj.recv(1024)
        msj = (mensaje.decode())
        if(msj== "cerrar servidor"):
            break
        archivo.write("Mensaje: " +msj+"\n")
        respuesta = ("ack")
        obj.send(respuesta.encode())

#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()
