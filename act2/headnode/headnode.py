from time import sleep
import socket
import os.path
import random
import time
import threading
from _thread import *

IP_HOST = '0.0.0.0'
PORT = 5000

socket_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cli.bind((IP_HOST,PORT))
socket_cli.listen(10)

datanodes = ['172.1.1.11','172.1.1.12','172.1.1.13']
nodos_vivos = ''

def Main(socket_c,addr):
    global nodos_vivos
    while True:
        m_recibido = socket_c.recv(1024)
        if not m_recibido:
            print("Closing connection with", client_address)
            socket_c.close()
            break
        m_recibido = m_recibido.decode('utf-8').strip()

        if m_recibido == 'Cerrar_Servidor':
            print("Cerrando Servidor")
            socket_c.close()
            break

        while True:
            random_node = random.randint(0,2)
            if str(random_node+1) in nodos_vivos:
                break
            

        random_node = random.randint(0,2)
        IP_HOST_D = datanodes[random_node]
        PORT_D = 5000
        print("Seleccionado nodo ", random_node+1)
        socket_datanode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_datanode.connect((IP_HOST_D,PORT_D))
        socket_datanode.send(m_recibido.encode('utf-8'))

        respuesta_dn = socket_datanode.recv(1024)
        respuesta_dn = respuesta_dn.decode('utf-8').strip()

        if (respuesta_dn == "ACK"):
            archivo_registro = open("registro_server.txt","a")
            archivo_registro.write("Mensaje " + m_recibido +  " Guardado en el Datanode " + str(random_node+1) + "\n") #################
            archivo_registro.close()
            socket_c.send(("Mensaje Contenido en datanode " + str(random_node+1)).encode('utf-8'))



def enviar_multicast():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 10000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(0.2)
    global nodos_vivos
    try:
        while True:
            time.sleep(5)
            nodos_vivos = ""
            sock.sendto("status?".encode(), (MCAST_GRP, MCAST_PORT))
            while True:
                try:
                    data, server = sock.recvfrom(1024)
                    data = data.decode('utf-8').strip()
                    nodos_vivos += data
                    print (nodos_vivos)
                    archivo_hb = open("hearbeat_server.txt", "a")
                    archivo_hb.write(time.strftime("%c") + "   El Nodo "+ data + " se encuentra activo" + "\n")
                    archivo_hb.close()

                except socket.timeout:
                    break
    finally:
        sock.close()

start_new_thread(enviar_multicast, ())

while True:
    connection, client_address = socket_cli.accept()
    print('connection from', client_address)
    start_new_thread(Main, (connection, client_address,))
