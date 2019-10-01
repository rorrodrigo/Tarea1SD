import socket
import os.path

host = 'localhost'
puerto = int(input("Ingrese el puerto:(5001/5002/5003)"))

#Creación socket (lado cliente)
obj = socket.socket()
#Conexión con el servidor.
obj.connect((host, puerto))

reg = "data.txt"
if (os.path.isfile(reg)):
    archivo = open(reg,"a")
else:
    archivo = open(reg,"w")

while True:
    mensaje = obj.recv(1024)
    print("Mensaje:" + mensaje.decode())
    archivo.write("Mensaje: " + mensaje.decode() +"\n")
    archivo.write(mensaje.decode())
    respuesta = ("Guardado exitoso!")
    obj.send(respuesta.encode())

#Cerramos la instancia del objeto servidor
obj.close()
archivo.close()
