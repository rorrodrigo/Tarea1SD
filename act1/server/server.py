import socket

log = "log.txt"
archivo = open(log,"w")
#instanciamos un objeto para trabajar con el socket
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Puerto y servidor que debe escuchar
ser.bind(('0.0.0.0', 5000))

flag = True
while flag:
    #Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
    ser.listen(5)
    print("Esperando conexiones...")

    #Instanciamos un objeto cli (socket cliente) para recibir datos
    cli, addr = ser.accept()
    print("Nueva conexion del cliente ",addr[0])

    while True:
        #Recibimos el mensaje
        recibido = cli.recv(1024)
        #Si se reciben datos nos muestra la IP y el mensaje recibido
        print ("IP: " + str(addr[0]) + " Mensaje:" + recibido.decode())
        archivo.write("IP: " + str(addr[0]) + "| Mensaje: " + recibido.decode()+"\n")
        cli.send("Mensaje recibido".encode())
        if(recibido.decode() == "salir"):
            cli.close()
            print ("Cliente desconectado")
            break
        elif(recibido.decode() == "cerrar servidor"):
            cli.close()
            ser.close()
            print("Cliente desconectado")
            flag = False
            break
        #Devolvemos el mensaje al cliente

archivo.close()
print("Servidor finalizado")
