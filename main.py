import pygame
import settings

pygame.init()

window_size = (1000, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Objetos en movimiento")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()