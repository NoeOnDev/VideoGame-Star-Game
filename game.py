import pygame
import sys
import socket

BACKGROUND_COLOR = (0, 0, 0)
SCREEN_SIZE = (800, 400)
PLAYER_SPEED = 1
FPS = 60

pygame.init()

ventana = pygame.display.set_mode(SCREEN_SIZE)

player_image = pygame.image.load('./src/img/nave.png')
player_image = pygame.transform.scale(player_image, (50, 30))

player_rect = player_image.get_rect()

clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

running = True
while running:
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

    client.send(f'{player_rect.x},{player_rect.y}'.encode())

    other_player_position = client.recv(1024).decode()
    other_player_x, other_player_y = map(int, other_player_position.split(','))

    ventana.fill(BACKGROUND_COLOR)

    ventana.blit(player_image, player_rect)

    other_player_rect = player_image.get_rect(topleft=(other_player_x, other_player_y))
    ventana.blit(player_image, other_player_rect)

    pygame.display.flip()

    clock.tick(FPS)