import asyncio
import websockets
import pygame
from pygame.locals import *
import json
import time

server_ip = '44.196.162.180'
server_port = 9009

pygame.init()
screen = pygame.display.set_mode((850, 530))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)

estado_jugador = {'x': 400, 'y': 300, 'ready': False, 'latency': 0}

estado_global = {}
meteoritos = []

background = pygame.image.load('./src/img/space.jpg')

tiempo_restante = 120  # Tiempo restante en segundos

async def actualizar_estado(websocket):
    global estado_global, meteoritos

    data = await websocket.recv()
    if data:
        estado = json.loads(data)
        estado_global = estado['estado_global']
        meteoritos = estado.get('meteoritos', [])

async def enviar_movimiento(websocket):
    start_time = time.time()
    await websocket.send(json.dumps(estado_jugador))
    await actualizar_estado(websocket)
    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)
    estado_jugador['latency'] = latency_ms

async def main():
    global tiempo_restante
    async with websockets.connect(f"ws://{server_ip}:{server_port}") as websocket:
        running = True
        start_time = time.time()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    estado_jugador['ready'] = not estado_jugador['ready']
                    await enviar_movimiento(websocket)
            
            keys = pygame.key.get_pressed()
            
            if keys[K_LEFT] and estado_jugador['x'] > 0:
                estado_jugador['x'] -= 5
            if keys[K_RIGHT] and estado_jugador['x'] < 830:
                estado_jugador['x'] += 5
            if keys[K_UP] and estado_jugador['y'] > 0:
                estado_jugador['y'] -= 5
            if keys[K_DOWN] and estado_jugador['y'] < 510:
                estado_jugador['y'] += 5

            await enviar_movimiento(websocket)

            screen.blit(background, (0, 0))

            for id_jugador, pos in estado_global.items():
                jugador = pygame.draw.rect(screen, (255, 0, 0), (pos['x'], pos['y'], 20, 20))
                
                gamertag = font.render(f'Player {id_jugador}', True, (255, 255, 255))
                screen.blit(gamertag, (pos['x'], pos['y'] - 20))

            for meteoro in meteoritos:
                pygame.draw.circle(screen, (255, 255, 255), (int(meteoro['x']), int(meteoro['y'])), 10)

            jugadores_listos = sum(1 for jugador in estado_global.values() if 'ready' in jugador and jugador['ready'])
            total_jugadores = len(estado_global)
            if jugadores_listos < total_jugadores:
                mensaje = f'JUGADORES LISTOS ({jugadores_listos}/{total_jugadores})'
            else:
                mensaje = '¡TODOS LOS JUGADORES ESTÁN LISTOS!'

            texto_mensaje = font.render(mensaje, True, (255, 255, 255))
            screen.blit(texto_mensaje, (10, 10))

            latency_text = font.render(f'{estado_jugador["latency"]} ms', True, (255, 255, 255))
            screen.blit(latency_text, (850 - latency_text.get_width() - 10, 10))

            current_time = time.time()
            elapsed_time = current_time - start_time
            tiempo_restante = 120 - int(elapsed_time)

            if tiempo_restante <= 0:
                estado_jugador = {'x': 400, 'y': 300, 'ready': False, 'latency': 0}
                estado_global = {}
                meteoritos = []
                tiempo_restante = 120
                start_time = time.time()

            timer_text = font.render(f'Tiempo restante: {tiempo_restante} s', True, (255, 255, 255))
            screen.blit(timer_text, (850 - timer_text.get_width() - 10, 30))

            pygame.display.update()

            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())