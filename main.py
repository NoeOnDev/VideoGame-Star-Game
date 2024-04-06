import pygame
import sys

pygame.init()

window_main_width = 800
window_main_height = 470

screen = pygame.display.set_mode((window_main_width, window_main_height))

background = pygame.image.load('./src/img/home.jpg')

start_button_color = (92, 169, 63)
exit_button_color = (193, 49, 49)
border_color = (23, 23, 23)

button_width = 150
button_height = 60
border_width = 5

start_button_x = window_main_width / 2 - button_width / 2
start_button_y = window_main_height / 2 - button_height / 2
exit_button_x = window_main_width / 2 - button_width / 2
exit_button_y = start_button_y + button_height + 30

screen.blit(background, (0, 0))

pygame.draw.rect(screen, border_color, pygame.Rect(start_button_x - border_width, start_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(exit_button_x - border_width, exit_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))

font = pygame.font.Font(None, 36)

start_text = font.render('Play', True, (0, 0, 0))
exit_text = font.render('Exit', True, (0, 0, 0))

game_name_font = pygame.font.Font(None, 72)
game_name_text = game_name_font.render('My Star', True, (255, 255, 255))
game_name_x = window_main_width / 2 - game_name_text.get_width() / 2
game_name_y = start_button_y / 2 - game_name_text.get_height() / 2
screen.blit(game_name_text, (game_name_x, game_name_y))

screen.blit(start_text, (start_button_x + (button_width - start_text.get_width()) // 2, start_button_y + (button_height - start_text.get_height()) // 2))
screen.blit(exit_text, (exit_button_x + (button_width - exit_text.get_width()) // 2, exit_button_y + (button_height - exit_text.get_height()) // 2))

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