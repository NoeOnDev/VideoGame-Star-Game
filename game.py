import socket
import pygame
from pygame.locals import *
import json

server_ip = '44.196.162.180'
server_port = 9009

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

pygame.init()
screen = pygame.display.set_mode((850, 530))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)

estado_jugador = {'x': 400, 'y': 300, 'ready': False}

estado_global = {}

background = pygame.image.load('./src/img/space.jpg')

def actualizar_estado():
    global estado_global
    data = client.recv(1024)
    if data:
        for line in data.decode().split('\n'):
            if line:
                estado_global = json.loads(line)

def enviar_movimiento():
    client.send((json.dumps(estado_jugador) + '\n').encode())

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                estado_jugador['ready'] = not estado_jugador['ready']
                enviar_movimiento()
        
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT] and estado_jugador['x'] > 0:
            estado_jugador['x'] -= 5
        if keys[K_RIGHT] and estado_jugador['x'] < 830:
            estado_jugador['x'] += 5
        if keys[K_UP] and estado_jugador['y'] > 0:
            estado_jugador['y'] -= 5
        if keys[K_DOWN] and estado_jugador['y'] < 510:
            estado_jugador['y'] += 5

        enviar_movimiento()

        actualizar_estado()

        screen.blit(background, (0, 0))

        cuadro_verde = pygame.draw.rect(screen, (0, 255, 0), (0, 300-50, 20, 20))

        for id_jugador, pos in estado_global.items():
            jugador = pygame.draw.rect(screen, (255, 0, 0), (pos['x'], pos['y'], 20, 20))
            
            gamertag = font.render(f'Player {id_jugador}', True, (255, 255, 255))
            screen.blit(gamertag, (pos['x'], pos['y'] - 20))

            if jugador.colliderect(cuadro_verde):
                print(f'Player {id_jugador} ha colisionado')

        jugadores_listos = sum(1 for jugador in estado_global.values() if 'ready' in jugador and jugador['ready'])
        total_jugadores = len(estado_global)
        if jugadores_listos < total_jugadores:
            mensaje = f'JUGADORES LISTOS ({jugadores_listos}/{total_jugadores})'
        else:
            mensaje = '¡TODOS LOS JUGADORES ESTÁN LISTOS!'

        texto_mensaje = font.render(mensaje, True, (255, 255, 255))
        screen.blit(texto_mensaje, (10, 10))

        pygame.display.update()

        clock.tick(60)

    client.close()
    pygame.quit()

if __name__ == '__main__':
    main()