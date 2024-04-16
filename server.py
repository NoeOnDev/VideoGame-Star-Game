import socket
import threading
import json

server_ip = '0.0.0.0'
server_port = 9009

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(2)

clientes = []

estado_global = {}

def manejar_cliente(cliente, id_jugador):
    global estado_global
    try:
        while True:
            datos = cliente.recv(1024)
            if not datos:
                break

            # Divide el mensaje por el carácter de nueva línea y decodifica cada línea por separado
            for line in datos.decode().split('\n'):
                if line:  # Ignora las líneas vacías
                    movimiento = json.loads(line)

                    estado_global[id_jugador] = movimiento
                    
                    for c in clientes:
                        c.send((json.dumps(estado_global) + '\n').encode())
    except ConnectionResetError:
        print("La conexión con el cliente ha sido cerrada inesperadamente.")
    finally:
        cliente.close()
        clientes.remove(cliente)

def aceptar_clientes():
    id_jugador = 0
    while True:
        cliente, addr = server.accept()
        print(f"Conexión desde {addr}")
        
        estado_global[id_jugador] = {'x': 400, 'y': 300}
        
        clientes.append(cliente)
        
        threading.Thread(target=manejar_cliente, args=(cliente, id_jugador)).start()
        
        id_jugador += 1

aceptar_clientes()
