import asyncio
import websockets
import json
import random

server_ip = '0.0.0.0'
server_port = 9009

clientes = set()

estado_global = {}

contador_jugadores = 0

meteoritos = []

def crear_meteoros():
    for _ in range(5):
        meteoro = {
            'x': random.randint(0, 850),
            'y': random.randint(-100, -10),
            'velocidad_x': random.uniform(-1, 1),
            'velocidad_y': random.uniform(2, 5)
        }
        meteoritos.append(meteoro)

async def manejar_cliente(websocket, path):
    global contador_jugadores
    id_jugador = contador_jugadores
    contador_jugadores += 1
    estado_global[id_jugador] = {'x': 400, 'y': 300, 'ready': False}
    clientes.add(websocket)
    print(f"Player {id_jugador} se ha unido al servidor.")

    try:
        while True:
            datos = await websocket.recv()
            movimiento = json.loads(datos)
            estado_global[id_jugador] = movimiento
    except websockets.ConnectionClosed:
        print(f"La conexión con el cliente {id_jugador} ha sido cerrada inesperadamente.")
    finally:
        clientes.remove(websocket)
        if id_jugador in estado_global:
            del estado_global[id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

async def actualizar_estado():
    crear_meteoros()

    while True:
        for meteoro in meteoritos:
            meteoro['x'] += meteoro['velocidad_x']
            meteoro['y'] += meteoro['velocidad_y']

        meteoritos[:] = [meteoro for meteoro in meteoritos if meteoro['y'] < 530]

        estado = {
            'estado_global': estado_global,
            'meteoritos': meteoritos
        }

        estado_json = json.dumps(estado)
        
        if clientes:
            tareas = [asyncio.create_task(cliente.send(estado_json)) for cliente in clientes if cliente.open]
            if tareas:
                await asyncio.wait(tareas)

        await asyncio.sleep(0.1)

start_server = websockets.serve(manejar_cliente, server_ip, server_port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(actualizar_estado())
loop.run_forever()
