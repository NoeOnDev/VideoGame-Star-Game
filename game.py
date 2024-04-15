import pygame
import sys

BACKGROUND_COLOR = (0, 0, 0)
SCREEN_SIZE = (800, 400)
PLAYER_SPEED = 1
FPS = 60

pygame.init()

ventana = pygame.display.set_mode(SCREEN_SIZE)

player_image = pygame.image.load('./src/img/nave.png')
player_image = pygame.transform.scale(player_image, (50, 30))

player_rect = player_image.get_rect()

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

    ventana.fill(BACKGROUND_COLOR)
    
    ventana.blit(player_image, player_rect)

    pygame.display.flip()