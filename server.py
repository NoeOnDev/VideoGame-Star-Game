import socket
import threading
import json

server_ip = 'localhost'
server_port = 12345

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

            movimiento = json.loads(datos.decode())

            estado_global[id_jugador] = movimiento

            for c in clientes:
                if c != cliente:
                    c.send(json.dumps(estado_global).encode())
    except (ConnectionResetError, BrokenPipeError):
        print(f"Error en la conexión con el cliente {id_jugador}. Desconectando.")
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
