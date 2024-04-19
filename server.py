import asyncio
import websockets
import json
import random
import time

server_ip = '0.0.0.0'
server_port = 9009

clientes = set()

estado_global = {}

contador_jugadores = 0

meteoritos = []

todos_listos = False

tiempo_restante = 0

# Función para verificar si todos los jugadores están listos
def verificar_todos_listos():
    global todos_listos
    todos_listos = all(jugador['ready'] for jugador in estado_global.values())

# Función para generar meteoros desde la parte derecha
async def generar_meteoros():
    intervalo = 1

    while True:
        if todos_listos and tiempo_restante > 0:
            meteoro = {
                'x': 850,
                'y': random.randint(0, 530),
                'velocidad_x': random.uniform(-2, -5),
                'velocidad_y': 0
            }
            meteoritos.append(meteoro)
        
        await asyncio.sleep(intervalo)

# Manejo de los clientes
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
                # Si algún jugador deja de estar listo, reinicia el temporizador
                tiempo_restante = 0
                meteoritos.clear()

    except websockets.ConnectionClosed:
        print(f"La conexión con el cliente {id_jugador} ha sido cerrada inesperadamente.")
    finally:
        clientes.remove(websocket)
        if id_jugador in estado_global:
            del estado_global[id_jugador]
            print(f"Player {id_jugador} ha sido eliminado")

# Función para verificar colisiones entre jugadores y meteoros
def verificar_colisiones():
    global tiempo_restante
    for id_jugador, jugador in estado_global.items():
        x_jugador = jugador['x']
        y_jugador = jugador['y']
        
        for meteoro in meteoritos:
            x_meteoro = meteoro['x']
            y_meteoro = meteoro['y']
            
            # Verifica si el jugador colisiona con un meteoro
            if (x_jugador - x_meteoro) ** 2 + (y_jugador - y_meteoro) ** 2 < 400:  # Radio de colisión
                tiempo_restante = 0  # Detener el juego en caso de colisión
                return

# Función para actualizar el estado de los meteoros y jugadores
async def actualizar_estado():
    global tiempo_restante

    while True:
        verificar_todos_listos()

        if todos_listos and tiempo_restante == 0:
            # Iniciar el temporizador si todos los jugadores están listos
            tiempo_restante = 120  # 2 minutos en segundos
            asyncio.create_task(generar_meteoros())
        
        if todos_listos and tiempo_restante > 0:
            # Actualizar el temporizador
            tiempo_restante -= 0.1  # Decrementar el tiempo restante
            
            # Verificar colisiones entre jugadores y meteoros
            verificar_colisiones()

            if tiempo_restante <= 0:
                # Si el tiempo restante se acaba, detener el juego
                tiempo_restante = 0
                meteoritos.clear()
        
        # Actualizar la posición de los meteoros
        for meteoro in meteoritos:
            meteoro['x'] += meteoro['velocidad_x']
            meteoro['y'] += meteoro['velocidad_y']

        # Eliminar meteoros que salen de la pantalla por la izquierda
        meteoritos[:] = [meteoro for meteoro in meteoritos if meteoro['x'] > 0]

        # Combina los estados de los jugadores y los meteoros
        estado = {
            'estado_global': estado_global,
            'meteoritos': meteoritos,
            'tiempo_restante': tiempo_restante
        }

        # Convierte el estado a JSON
        estado_json = json.dumps(estado)
        
        # Envía el estado a los clientes
        if clientes:
            tareas = [asyncio.create_task(cliente.send(estado_json)) for cliente in clientes if cliente.open]
            if tareas:
                await asyncio.wait(tareas)

        await asyncio.sleep(0.1)

# Inicialización del servidor
start_server = websockets.serve(manejar_cliente, server_ip, server_port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(actualizar_estado())
loop.run_forever()
