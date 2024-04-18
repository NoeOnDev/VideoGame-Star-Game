import socket
import asyncio
import json

server_ip = '0.0.0.0'
server_port = 9009

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(2)
server.setblocking(False)

clientes = []

estado_global = {}

async def manejar_cliente(cliente, id_jugador):
    global estado_global
    try:
        while True:
            datos = await loop.sock_recv(cliente, 4096)
            if not datos:
                break

            for line in datos.decode().split('\n'):
                if line:
                    movimiento = json.loads(line)

                    estado_global[id_jugador] = movimiento
                    
                    for c in clientes:
                        await loop.sock_sendall(c, (json.dumps(estado_global) + '\n').encode())
    except ConnectionResetError:
        print("La conexión con el cliente ha sido cerrada inesperadamente.")
    finally:
        cliente.close()
        clientes.remove(cliente)
        if id_jugador in estado_global:
            del estado_global[id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

async def aceptar_clientes():
    id_jugador = 0
    while True:
        cliente, addr = await loop.sock_accept(server)
        print(f"Conexión desde {addr}")
        
        estado_global[id_jugador] = {'x': 400, 'y': 300, 'listo': False}
        
        clientes.append(cliente)
        
        loop.create_task(manejar_cliente(cliente, id_jugador))
        
        id_jugador += 1

loop = asyncio.get_event_loop()
loop.run_until_complete(aceptar_clientes())