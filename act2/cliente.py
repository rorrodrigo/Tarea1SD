import socket
import os.path

host = input("Ingrese la direccion IP: ")
puerto = int(input("Ingrese el puerto: "))

#host = 'localhost'
#puerto = 5000

#Creación socket (lado cliente)
obj = socket.socket()
 
#Conexión con el servidor.
obj.connect((host, puerto))
print("Conexión establecida")

respuestas = "respuestas.txt"
if (os.path.isfile(respuestas)):
    archivo = open(respuestas,"a")
else:
    archivo = open(respuestas,"w")
 
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = input("Mensaje   >> ")
    #Con el método send, enviamos el mensaje
    obj.send(mensaje.encode())
    if(mensaje == "salir"):
        break
    elif(mensaje == "cerrar servidor"):
        break
    respuesta = obj.recv(1024)
    print("Respuesta >> " + respuesta.decode())
    archivo.write("Respuesta: " + respuesta.decode()+"\n")

#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
print("Fin de Conexión")