import socket

IP_HOST = '172.1.1.10'
PORT = 5000
print("Cliente Conectado Con el Servidor")

archivo = open("registro_cliente.txt","a")
Mensajes = ['Hola','Como','Estas','Adios','Cerrar_Servidor']

socket_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cli.connect((IP_HOST,PORT))

for mensaje in Mensajes:
    socket_cli.send(mensaje.encode('utf-8'))
    respuesta = socket_cli.recv(1024)
    respuesta = respuesta.decode('utf-8')
    archivo.write(respuesta + "\n")

socket_cli.close()
archivo.close()

print("Fin de Conexion")
