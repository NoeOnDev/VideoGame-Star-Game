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

todos_listos = False

tarea_generar_meteoros = None

def verificar_todos_listos():
    global todos_listos
    todos_listos = all(jugador['ready'] for jugador in estado_global.values())

async def generar_meteoros():
    intervalo = 1

    while True:
        if todos_listos and len([jugador for jugador in estado_global.values() if jugador['ready']]) > 0:
            meteoro = {
                'x': 850,
                'y': random.randint(0, 530),
                'velocidad_x': random.uniform(-2, -5),
                'velocidad_y': 0
            }
            meteoritos.append(meteoro)
        
        await asyncio.sleep(intervalo)

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
    global tarea_generar_meteoros
    while True:
        verificar_todos_listos()
        
        if todos_listos and tarea_generar_meteoros is None:
            tarea_generar_meteoros = asyncio.create_task(generar_meteoros())

        if todos_listos and not any(isinstance(t, asyncio.Task) and not t.done() for t in asyncio.all_tasks()):
            asyncio.create_task(generar_meteoros())

        for meteoro in meteoritos:
            meteoro['x'] += meteoro['velocidad_x']
            meteoro['y'] += meteoro['velocidad_y']

        meteoritos[:] = [meteoro for meteoro in meteoritos if meteoro['x'] > 0]

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
