from time import sleep
import socket
import os.path
import random
import time
import threading

kill = False

global mutex
mutex = threading.Lock()
mutex.acquire()
mutex.release()

def enviar_multicast():
    global kill
    if(kill == True):
        return
    else:
        threading.Timer(5.0, enviar_multicast).start()
        #print("empezo el multi\n")
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.settimeout(0.5)
        vivos = ""
        try:
            sock.sendto("status".encode(), (MCAST_GRP, MCAST_PORT))
            while True:
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    data = "".encode()
                    break
                finally:
                    vivos += data.decode()
        finally:
            reg = "hearbeat_server.txt"
            if (os.path.isfile(reg)):
                mutex.acquire()
                archivo = open(reg, "a")
            else:
                mutex.acquire()
                archivo = open(reg, "w")
            archivo.write(time.strftime("%c") + "@" + vivos + "\n")
            archivo.close()
            mutex.release()
            sock.close()

#instanciamos un objeto para trabajar con el cliente
ser_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host="localhost"
port = 5000
ser_cli.bind((host, port))

#lista con conexiones a los datanodes
datanodes = []

ser_dn1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_dn1.bind(('localhost', 5001))
ser_dn1.listen(1)
print("Esperando al datanode 1...")
cli1, addr1 = ser_dn1.accept()
datanodes.append((ser_dn1,cli1,addr1))

#ser_dn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ser_dn2.bind(('0.0.0.0', 5002))
#ser_dn2.listen(1)
#print("Esperando al datanode 2...")
#cli2, addr2 = ser_dn2.accept()
#datanodes.append((ser_dn2,cli2,addr2))

#ser_dn3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ser_dn3.bind(('0.0.0.0', 5003))
#ser_dn3.listen(1)
#print("Esperando al datanode 3... ")
#cli3, addr3 = ser_dn3.accept()
#datanodes.append((ser_dn3,cli3,addr3))

enviar_multicast()
flag = True
while flag:
    #Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
    ser_cli.listen(5)
    print("Esperando conexiones...")
    cli, addr = ser_cli.accept()

    while True:
        #Recibimos el mensaje
        recibido = cli.recv(1024)
        rcb = recibido.decode()
        if(recibido.decode() == "salir"):
            cli.close()
            break
        elif(recibido.decode() == "cerrar servidor"):
            cli.send(("Servidor Cerrado Correctamente").encode())
            cli1.send(("cerrar servidor").encode())
            #cli2.send(("cerrar servidor").encode())
            #cli3.send(("cerrar servidor").encode())
            cli1.close()
            #cli2.close()
            #cli3.close()
            cli.close()
            ser_cli.close()
            ser_dn1.close()
            #ser_dn2.close()
            #ser_dn3.close()
            flag = False
            kill = True
            break
        #Si se reciben datos nos muestra la IP y el mensaje recibido
        #print ("IP: " + str(addr[0]) + " Mensaje:" + recibido.decode())

        flag = True
        while flag:
            flag2 = True
            while(flag2):
                try:
                    mutex.acquire()
                    archivo = open("hearbeat_server.txt","r")
                    flag2 = False
                except:
                    mutex.release()
                    flag2 = True

            linea = archivo.readlines()[-1]
            archivo.close()
            mutex.release()
            l = linea.strip().split("@")
            l2 = l[1].strip().split("-")
            l2.remove("")
            if( len(l2) == 0):
                continue
            rand = int(random.choice(l2))
            #enviar mensaje al datanode
            ser_dn,cli_dn,addr_dn = datanodes[rand-1]
            cli_dn.send(rcb.encode())
            #esperar la respuesta desde el datanode de guardado exitoso
            ser_dn.settimeout(0.2)
            try:
                respuesta_dn = cli_dn.recv(1024)
                if(respuesta_dn.decode() == "ack"):
                    #print(respuesta_dn.decode())
                    flag = False
            except socket.timeout:
                flag = True

        reg2 = "registro_server.txt"
        if (os.path.isfile(reg2)):
            archivo2 = open(reg2,"a")
        else:
            archivo2 = open(reg2,"w")
        archivo2.write("IP: "+ str(addr[0])+ " - Mensaje: " + recibido.decode() + " - DataNode: " + str(rand) + "\n")
        archivo2.close()
        #Devolvemos un mensaje al cliente (el datanode que almacena su mensaje)
        cli.send(("Mensaje Contenido en datanode " + str(rand)).encode())

print("Servidor finalizado")
