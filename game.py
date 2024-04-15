import pygame
import sys
import socket

BACKGROUND_COLOR = (0, 0, 0)
SCREEN_SIZE = (800, 400)
PLAYER_SPEED = 1
FPS = 60

pygame.init()

ventana = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Juego de Nave')

player_image = pygame.image.load('./src/img/nave.png')
player_image = pygame.transform.scale(player_image, (50, 30))

player_rect = player_image.get_rect()

clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

other_player_x, other_player_y = 0, 0
running = True

while running:
    ventana.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_rect.y += PLAYER_SPEED

    try:
        position_message = f'{player_rect.x},{player_rect.y}'
        client.send(position_message.encode())
    except BrokenPipeError:
        print("La conexión con el servidor se ha perdido.")
        client.close()
        running = False
        continue

    try:
        other_player_position = client.recv(1024).decode()
        if other_player_position:
            print(f"Recibida posición de otro jugador: {other_player_position}")
            other_player_x, other_player_y = map(int, other_player_position.split(','))
    except Exception as e:
        print(f"Error al recibir datos del servidor: {e}")

    ventana.blit(player_image, player_rect)

    other_player_rect = player_image.get_rect(topleft=(other_player_x, other_player_y))
    ventana.blit(player_image, other_player_rect)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
sys.exit()
