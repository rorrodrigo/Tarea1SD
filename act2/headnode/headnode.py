from time import sleep
import socket
import random
import time
import threading
from _thread import *

#Config Socket cliente-server
IP_HOST = '0.0.0.0'
PORT = 5000

#Se crea el socket server y queda en espera a nuevas conecciones
socket_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cli.bind((IP_HOST,PORT))
socket_cli.listen(5)

#Lista de IP's de los Datanodes
datanodes = ['172.1.1.11','172.1.1.12','172.1.1.13']

nodos_vivos = "" #String auxiliar para realizar la seleccion del random_node mas adelante

### Definicion de la funcion Main del Headnode
def Main(socket_c,addr):
    global nodos_vivos
    while True:
        #Se espera por el mensaje del cliente y se decodifica
        m_recibido = socket_c.recv(1024)
        m_recibido = m_recibido.decode()

        #En el caso de que el cliente escriba salir se cierra el socket cliente-server
        if m_recibido == 'Salir':
            socket_c.close()
            sleep(1)
            print ("Cliente Desconectado")
            break
        #Se determina de forma aleatoria entre todos los nodos activos, el datanode donde se guardara el mensaje
        while True:
            random_node = random.randint(0,2)
            if str(random_node+1) in nodos_vivos:
                break
        #Config de la IP_HOST para el socket server-datanode seleccioando
        IP_HOST_D = datanodes[random_node]

        #Se crea el socket server-datanode, se conecta y le envia el mensaje del cliente al datanode seleccionado
        socket_datanode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_datanode.connect((IP_HOST_D,PORT))
        socket_datanode.send(m_recibido.encode())

        #Se espera por la respuesta del datanode y se decodifica
        respuesta_dn = socket_datanode.recv(1024)
        respuesta_dn = respuesta_dn.decode()

        #Si el datanode recibio correctamente el mensaje , se escribe en el archivo y se envía el mensaje al cliente de donde se guardó su mensaje
        if (respuesta_dn == "ACK"):
            archivo_registro = open("registro_server.txt","a")
            archivo_registro.write("Mensaje '" +  m_recibido +  "' Guardado en el Datanode " + str(random_node+1) + "\n")
            archivo_registro.close()
            socket_c.send(("Mensaje '" + m_recibido + "' Contenido en datanode " + str(random_node+1)).encode())


### Definicion de la funcion que envia los mensajes a los datanodes, mediante un mensaje multicast
def enviar_multicast():
    #Config del socket multicast
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(0.2)
    global nodos_vivos
    try:
        while True:
            time.sleep(5)
            nodos_vivos = ""
            sock.sendto("status?".encode(), (MCAST_GRP, MCAST_PORT)) # Se envia el mensaje a los datanodes
            while True:
                try:
                    data, server = sock.recvfrom(1024) #Se espera la respuesta de los datanodes
                    #Se decodifica la respuesta de los datanodes las cuales pueden ser "1" , "2" ,"3", que corresponden al nuemero del datanode
                    data = data.decode()
                    nodos_vivos += data #Se añade el numero del datanode al string de los datanodes activos
                    #Se escribe en el archivo que el datanode i esta activo
                    archivo_hb = open("hearbeat_server.txt", "a")
                    archivo_hb.write(time.strftime("%c") + "   El Nodo "+ data + " se encuentra activo" + "\n")
                    archivo_hb.close()
                #Si no hay respuesta del datanode
                except socket.timeout:
                    break
    finally:
        sock.close()

#Se crea el thread para el envio de los mensajes multicast
start_new_thread(enviar_multicast, ())

#Se crea el while para la coneccion de los clientes
while True:
    cliente, address = socket_cli.accept()
    print("Nueva conexion del cliente: ",address[0])
    #Se crea el thread de la conexion cliente-servidor
    start_new_thread(Main, (cliente, address,))
