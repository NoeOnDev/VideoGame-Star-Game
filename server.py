import socket
import asyncio
import json
import random

server_ip = '0.0.0.0'
server_port = 9009

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(2)
server.setblocking(False)

clientes = []

estado_global = {
    'jugadores': {},
    'asteroides': []
}

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

                    estado_global['jugadores'][id_jugador] = movimiento
                    
                    for c in clientes:
                        await loop.sock_sendall(c, (json.dumps(estado_global) + '\n').encode())
    except ConnectionResetError:
        print("La conexión con el cliente ha sido cerrada inesperadamente.")
    finally:
        cliente.close()
        clientes.remove(cliente)
        if id_jugador in estado_global['jugadores']:
            del estado_global['jugadores'][id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

async def generar_asteroides():
    while True:
        jugadores_listos = all(jugador.get('ready', False) for jugador in estado_global['jugadores'].values())
        if jugadores_listos:
            await asyncio.sleep(2)
            if random.random() < 0.5:
                asteroide = {'x': 850, 'y': random.randint(0, 530), 'v': random.uniform(0.1, 0.5)}
                estado_global['asteroides'].append(asteroide)
        
        for asteroide in estado_global['asteroides']:
            if jugadores_listos:
                asteroide['x'] -= asteroide['v']
            else:
                estado_global['asteroides'] = []
        
        estado_global['asteroides'] = [asteroide for asteroide in estado_global['asteroides'] if asteroide['x'] > 0]
        
        await asyncio.sleep(1/60)

async def aceptar_clientes():
    id_jugador = 0
    while True:
        cliente, addr = await loop.sock_accept(server)
        print(f"Conexión desde {addr}")
        
        estado_global['jugadores'][id_jugador] = {'x': 400, 'y': 300, 'ready': False}
        
        clientes.append(cliente)
        
        loop.create_task(manejar_cliente(cliente, id_jugador))
        
        id_jugador += 1

loop = asyncio.get_event_loop()
loop.create_task(generar_asteroides())
loop.run_until_complete(aceptar_clientes())