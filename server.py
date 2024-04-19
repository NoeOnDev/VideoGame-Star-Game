import asyncio
import websockets
import json
import time

server_ip = '0.0.0.0'
server_port = 9009

clientes = set()

estado_global = {}

contador_jugadores = 0

async def manejar_cliente(websocket, path):
    global contador_jugadores
    id_jugador = contador_jugadores
    contador_jugadores += 1
    estado_global[id_jugador] = {'x': 400, 'y': 300, 'listo': False}
    clientes.add(websocket)
    print(f"Player {id_jugador} se ha unido al servidor.")
    try:
        while True:
            datos = await websocket.recv()
            movimiento = json.loads(datos)
            estado_global[id_jugador] = movimiento
    except websockets.ConnectionClosed:
        print("La conexión con el cliente ha sido cerrada inesperadamente.")
    finally:
        clientes.remove(websocket)
        if id_jugador in estado_global:
            del estado_global[id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

async def actualizar_estado():
    while True:
        estado = json.dumps(estado_global)
        if clientes:
            tareas = [cliente.send(estado) for cliente in clientes if cliente.open]
            if tareas:
                await asyncio.wait(tareas)
        await asyncio.sleep(0.1)

start_server = websockets.serve(manejar_cliente, server_ip, server_port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(actualizar_estado())
loop.run_forever()