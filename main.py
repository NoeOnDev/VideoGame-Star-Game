import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

start_button = pygame.image.load('./src/img/play.png')
exit_button = pygame.image.load('./src/img/quit.png')

screen.blit(start_button, (200, 200))
screen.blit(exit_button, (200, 300))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 200 <= x <= 200 + start_button.get_width() and 200 <= y <= 200 + start_button.get_height():
                print("Iniciar juego")
            elif 400 <= x <= 400 + exit_button.get_width() and 200 <= y <= 200 + exit_button.get_height():
                pygame.quit()
                sys.exit()