# Tarea1SD

Rodrigo Álvarez 201573587-5
Manuel Sandoval 201573604-9

Debido a que no fue posible crear un contenedor que permitiera ingresar los mensajes por consola, se usan mensajes predefinidos.
Cada archivo .py posee su propia carpeta donde guarda y maneja archivos que utiliza.

# Ejeccución de Actividades

Para ejecutar cada actividad, ir a la carpeta correspondiente a cada una, abrir un terminal y ejecutar los comandos:
  
  $ sudo docker-compose build 
  
  $ sudo docker-compose up
  
Para la segunda actividad, una vez finalizada la ejecución, como el cliente abandona el servidor, este ultimo quedará ejecutando el multicasting cada 5 segundos, por lo que se deberá usar ctrl+c para detener el proceso.

# Rutas de los archivos

## Actividad 1

### Archivo Cliente

    act1/client/respuestas.txt

### Archivo Servidor

    act1/server/logs.txt

## Actividad 2

### Archivos headnode

    act2/headnode/hearbeat_server.txt

    act2/headnode/registro_server.txt

### Archivo datanode_x

    act2/datanode{x}/data.txt

### Archivo cliente

    act2/client/registro_cliente.txt
