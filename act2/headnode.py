import socket
import os.path
from random import randint
import time
import threading

def multicast(lista_nodos):
    threading.Timer(5.0, multicast).start()
    reg = "hearbeat_server.txt"
    if (os.path.isfile(reg)):
        archivo = open(reg,"a")
    else:
        archivo = open(reg,"w")
    archivo.write(time.strftime("%c") + ": ")
    for nodo in lista_nodos:
        nodo.send("estado".encode())
        recibido = cli.recv(1024)
        if(recibido.decode() == "ok"):
            index = lista_nodos.index(nodo) + 1
            archivo.write(str(index))
    archivo.write("\n")
    archivo.close

reg = "hearbeat_server.txt"
if (os.path.isfile(reg)):
    archivo = open(reg,"a")
else:
    archivo = open(reg,"w")

#instanciamos un objeto para trabajar con el cliente
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host="localhost"
port = 5000

#Puerto y servidor que debe escuchar
ser.bind((host, port))

#crear los sockets de los datanodes

#lista con conexiones a los datanodes
nodos = []
for i in range(3):
    puerto = port+i+1
    #socket servidor
    obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    obj.bind((host, puerto))
    obj.listen(1)
    print("Esperando al datanode " + str(i+1) + "...")
    (cli, addr) = obj.accept()
    nodos.append(obj)

#print (nodos)

flag = True
while flag:
    #Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
    ser.listen(5)
    print("Esperando conexiones...")
    #multicast(nodos)

    #Instanciamos un objeto cli (socket cliente) para recibir datos
    (cli, addr) = ser.accept()
    while True:
        #Recibimos el mensaje
        recibido = cli.recv(1024)
        #Si se reciben datos nos muestra la IP y el mensaje recibido
        print ("IP: " + str(addr[0]) + " Mensaje:" + recibido.decode())
        archivo.write("IP: " + str(addr[0]) + " -  Mensaje:" + recibido.decode()+"\n")

        if(recibido.decode() == "salir"):
            cli.close()
            break
        elif(recibido.decode() == "cerrar servidor"):
            cli.close()
            for nodo in nodos:
                nodo.close()
            ser.close()
            flag = False
            break

        #almacenar el mensaje en un datanode aleatorio
        random = randint(0,2)

        reg2 = "registro_server.txt"
        if (os.path.isfile(reg2)):
            archivo2 = open(reg2,"a")
        else:
            archivo2 = open(reg2,"w")
        archivo2.write("IP: "+ str(addr[0])+ " - Mensaje: " + recibido.decode() + " - DataNode: " + str(random) + "\n")


        #Devolvemos un mensaje al cliente (el datanode que almacena su mensaje)
        cli.send(str(random).encode())

archivo.close()
archivo2.close()
print("Servidor finalizado")




#cliente-servidor
#el cliente crea un socket cliente que se conecta al socket servidor que ya debe estar esperando
    #y el cliente manda mensajes
