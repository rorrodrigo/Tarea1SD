import socket
from time import sleep

host = '0.0.0.0'
puerto = 5000

#Creación socket (lado cliente)
obj = socket.socket()

#Conexión con el servidor.
obj.connect((host, puerto))
respuestas = "respuestas.txt"
archivo = open(respuestas,"w")
mensajes = ['Hola','Como','Estas','xao','nos vimos','cerrar servidor']
i=0
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = mensajes[i]
    #Con el método send, enviamos el mensaje
    obj.send(mensaje.encode())
    respuesta = obj.recv(1024)
    archivo.write("Respuesta: " + respuesta.decode()+"\n")
    if(mensaje == "cerrar servidor"):
        break
    i+=1
#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
sleep(1)
print("Fin de Conexion")
