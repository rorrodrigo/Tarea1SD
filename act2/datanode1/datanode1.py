import socket
import os.path
import threading
import sys
import struct

kill = False

def responder_multicast():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    global kill
    while True:
        if(kill == True):
            return
        else:
            data, address = sock.recvfrom(1024)
            if(data.decode() == "status"):
                sock.sendto('1-'.encode(), address)

host = "localhost"
puerto = 5001

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
    t = threading.Thread(target=responder_multicast)
    t.start()
    while True:
        mensaje = obj.recv(1024)
        msj = (mensaje.decode())
        if(msj== "cerrar servidor"):
            kill = True
            break
        archivo.write(" Mensaje: " +msj+"\n")
        respuesta = ("ack")
        obj.send(respuesta.encode())

#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()
