import pygame
import sys

pygame.init()

window_main_width = 800
window_main_height = 470

screen = pygame.display.set_mode((window_main_width, window_main_height))

background = pygame.image.load('./src/img/home.jpg')

start_button_color = (0, 255, 0)
exit_button_color = (255, 0, 0)

button_width = 150
button_height = 70

start_button_x = window_main_width / 2 - button_width / 2
start_button_y = window_main_height / 2 - button_height / 2
exit_button_x = window_main_width / 2 - button_width / 2
exit_button_y = start_button_y + button_height + 30

screen.blit(background, (0, 0))

pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))
pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if start_button_x <= x <= start_button_x + button_width and start_button_y <= y <= start_button_y + button_height:
                print("Iniciar juego")
            elif exit_button_x <= x <= exit_button_x + button_width and exit_button_y <= y <= exit_button_y + button_height:
                pygame.quit()
                sys.exit()