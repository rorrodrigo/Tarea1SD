import socket
import os.path
import random

host = 'localhost'
puerto = 5000

#host = 'localhost'
#puerto = 5000

#Creación socket (lado cliente)
obj = socket.socket()

#Conexión con el servidor.
obj.connect((host, puerto))
print("Conexion establecida")

respuestas = "respuestas.txt"
# if (os.path.isfile(respuestas)):
#     archivo = open(respuestas,"a")
# else:
#     archivo = open(respuestas,"w")
archivo = open(respuestas,"w")
mensajes = ['Hola','Como','Estas','xao','nos vimos','dx','ok','pene','cerrar servidor']
i=0
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = mensajes[i]
    #Con el método send, enviamos el mensaje
    obj.send(mensaje.encode())
    print(mensaje)
    respuesta = obj.recv(1024)
    print("Respuesta >> " + respuesta.decode())
    archivo.write("Respuesta: " + respuesta.decode()+"\n")
    if(mensaje == "cerrar servidor"):
        break
    i+=1
#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
print("Fin de Conexion")
