import socket
import time

#Datos del Socket del Servidor
IP_HOST = '172.1.1.10'
PORT = 5000

archivo = open("registro_cliente.txt","a")

#Lista de Mensajes que se enviaran al servidor
Mensajes = ['Hola','Como','Estas','Probando','Tarea','GG','Docker','Para la Otra','Nos Sacamos','Un 100','Adios','Salir']

#Se crea el Socket Cliente-Servidor
socket_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cli.connect((IP_HOST,PORT))

for mensaje in Mensajes:
    socket_cli.send(mensaje.encode())  #Se envia el mensaje al servidor
    respuesta = socket_cli.recv(1024) #Se espera el mensaje de respuesta del servidor
    respuesta = respuesta.decode() #Se extrae el mensaje
    archivo.write(respuesta + "\n") #Se escribe el mensaje que contiene en cual de los datanodes se guardó el mensaje

#Se cierra el socket y el archivo
print ("Todos los Mensajes se han enviado y guardado")
print ("Desconectandose del Servidor ...")
socket_cli.close()
archivo.close()
