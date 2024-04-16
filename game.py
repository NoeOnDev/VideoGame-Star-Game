import socket
import pygame
from pygame.locals import *
import json

server_ip = '44.196.162.180'
server_port = 9009

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

estado_jugador = {'x': 400, 'y': 300}

estado_global = {}

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
        
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT]:
            estado_jugador['x'] -= 5
        if keys[K_RIGHT]:
            estado_jugador['x'] += 5
        if keys[K_UP]:
            estado_jugador['y'] -= 5
        if keys[K_DOWN]:
            estado_jugador['y'] += 5

        enviar_movimiento()

        actualizar_estado()

        screen.fill((0, 0, 0))

        for id_jugador, pos in estado_global.items():
            pygame.draw.rect(screen, (255, 0, 0), (pos['x'], pos['y'], 20, 20))

        pygame.display.update()

        clock.tick(60)

    client.close()
    pygame.quit()

if __name__ == '__main__':
    main()
