import socket
import os.path

reg = "log.txt"
if (os.path.isfile(log)):
    archivo = open(reg,"a")
else:
    archivo = open(reg,"w")

#instanciamos un objeto para trabajar con el socket
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#Puerto y servidor que debe escuchar
ser.bind(("localhost", 5000))

flag = True 
while flag:
    #Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
    ser.listen(1)
    print("Esperando conexiones...")

    #Instanciamos un objeto cli (socket cliente) para recibir datos
    cli, addr = ser.accept()

    while True:
        #Recibimos el mensaje
        recibido = cli.recv(1024)
        #Si se reciben datos nos muestra la IP y el mensaje recibido
        print ("IP: " + str(addr[0]) + " Mensaje:" + recibido.decode())
        archivo.write("IP: " + str(addr[0]) + "| Mensaje:" + recibido.decode()+"\n")

        if(recibido.decode() == "salir"):
            cli.close()
            break
        elif(recibido.decode() == "cerrar servidor"):
            cli.close()
            ser.close()
            flag = False
            break
        #Devolvemos el mensaje al cliente
        cli.send("Mensaje recibido".encode())

archivo.close()
print("Servidor finalizado")