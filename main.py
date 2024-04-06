import pygame
import sys

pygame.init()

window_main_width = 800
window_main_height = 501

screen = pygame.display.set_mode((window_main_width, window_main_height))

background = pygame.image.load('./src/img/background.png')

start_button = pygame.image.load('./src/img/play.png')
exit_button = pygame.image.load('./src/img/quit.png')

start_button = pygame.transform.scale(start_button, (150, 75))
exit_button = pygame.transform.scale(exit_button, (130, 50))

start_button_x = window_main_width / 2 - start_button.get_width() / 2
start_button_y = window_main_height / 2 - start_button.get_height() / 2
exit_button_x = window_main_width / 2 - exit_button.get_width() / 2
exit_button_y = start_button_y + start_button.get_height() + 30

screen.blit(background, (0, 0))

screen.blit(start_button, (start_button_x, start_button_y))
screen.blit(exit_button, (exit_button_x, exit_button_y))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if start_button_x <= x <= start_button_x + start_button.get_width() and start_button_y <= y <= start_button_y + start_button.get_height():
                print("Iniciar juego")
            elif exit_button_x <= x <= exit_button_x + exit_button.get_width() and exit_button_y <= y <= exit_button_y + exit_button.get_height():
                pygame.quit()
                sys.exit()