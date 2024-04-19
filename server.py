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

tiempo_restante = 0

def verificar_todos_listos():
    global todos_listos
    todos_listos = all(jugador['ready'] for jugador in estado_global.values())

async def generar_meteoros():
    intervalo = 1

    while True:
        if clientes and todos_listos and tiempo_restante > 0:
            num_meteoros = random.randint(0, 1)

            for _ in range(num_meteoros):
                meteoro = {
                    'x': 850,
                    'y': random.randint(0, 530),
                    'velocidad_x': random.uniform(-2, -5),
                    'velocidad_y': 0
                }
                meteoritos.append(meteoro)
        
        await asyncio.sleep(intervalo)

async def manejar_cliente(websocket, path):
    global contador_jugadores, tiempo_restante
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
            
            if not movimiento['ready'] and tiempo_restante > 0:
                tiempo_restante = 0
                meteoritos.clear()

    except websockets.ConnectionClosed:
        print(f"La conexión con el cliente {id_jugador} ha sido cerrada inesperadamente.")
    finally:
        clientes.remove(websocket)
        if id_jugador in estado_global:
            del estado_global[id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

def verificar_colisiones():
    global tiempo_restante
    for id_jugador, jugador in estado_global.items():
        x_jugador = jugador['x']
        y_jugador = jugador['y']
        
        for meteoro in meteoritos:
            x_meteoro = meteoro['x']
            y_meteoro = meteoro['y']
            
            if (x_jugador - x_meteoro) ** 2 + (y_jugador - y_meteoro) ** 2 < 400:
                tiempo_restante = 0
                return

async def actualizar_estado():
    global tiempo_restante

    while True:
        verificar_todos_listos()

        if todos_listos and tiempo_restante == 0:
            tiempo_restante = 120
            asyncio.create_task(generar_meteoros())
        
        if todos_listos and tiempo_restante > 0:
            tiempo_restante -= 0.1

            verificar_colisiones()

            if tiempo_restante <= 0:
                tiempo_restante = 0
                meteoritos.clear()
        
        for meteoro in meteoritos:
            meteoro['x'] += meteoro['velocidad_x']
            meteoro['y'] += meteoro['velocidad_y']

        meteoritos[:] = [meteoro for meteoro in meteoritos if meteoro['x'] > 0]

        estado = {
            'estado_global': estado_global,
            'meteoritos': meteoritos,
            'tiempo_restante': tiempo_restante
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
