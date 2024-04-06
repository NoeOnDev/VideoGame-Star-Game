import pygame
import sys

pygame.init()
pygame.mixer.init()

window_main_width = 800
window_main_height = 470

screen = pygame.display.set_mode((window_main_width, window_main_height))

background = pygame.image.load('./src/img/home.jpg')

start_button_color = (0, 255, 19)
exit_button_color = (255, 0, 0)
volume_up_button_color = (255, 255, 0)
volume_down_button_color = (255, 0, 0)
border_color = (23, 23, 23)

button_width = 200
button_height = 70
button_volume_width = 40
button_volume_height = 40
border_width = 5

start_button_x = window_main_width / 2 - button_width / 2
start_button_y = window_main_height / 2 - button_height / 2
exit_button_x = window_main_width / 2 - button_width / 2
exit_button_y = start_button_y + button_height + 30

volume_down_button_x = 5
volume_down_button_y = window_main_height - button_volume_height -10

volume_up_button_x = button_volume_width + 20
volume_up_button_y = window_main_height - button_volume_height -10

screen.blit(background, (0, 0))

pygame.draw.rect(screen, border_color, pygame.Rect(start_button_x - border_width, start_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(exit_button_x - border_width, exit_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(volume_up_button_x - border_width, volume_up_button_y - border_width, button_volume_width + 2 * border_width, button_volume_height + 2 * border_width))
pygame.draw.rect(screen, volume_up_button_color, pygame.Rect(volume_up_button_x, volume_up_button_y, button_volume_width, button_volume_height))

pygame.draw.rect(screen, border_color, pygame.Rect(volume_down_button_x - border_width, volume_down_button_y - border_width, button_volume_width + 2 * border_width, button_volume_height + 2 * border_width))
pygame.draw.rect(screen, volume_down_button_color, pygame.Rect(volume_down_button_x, volume_down_button_y, button_volume_width, button_volume_height))

font = pygame.font.Font(None, 40)

start_text = font.render('Play', True, (0, 0, 0))
exit_text = font.render('Exit', True, (0, 0, 0))
volume_up_text = font.render('+', True, (0, 0, 0))
volume_down_text = font.render('-', True, (0, 0, 0))

game_name_font = pygame.font.Font(None, 72)
game_name_text = game_name_font.render('My Star', True, (255, 255, 255))
game_name_x = window_main_width / 2 - game_name_text.get_width() / 2
game_name_y = start_button_y / 2 - game_name_text.get_height() / 2
screen.blit(game_name_text, (game_name_x, game_name_y))

screen.blit(start_text, (start_button_x + (button_width - start_text.get_width()) // 2, start_button_y + (button_height - start_text.get_height()) // 2))
screen.blit(exit_text, (exit_button_x + (button_width - exit_text.get_width()) // 2, exit_button_y + (button_height - exit_text.get_height()) // 2))
screen.blit(volume_up_text, (volume_up_button_x + (button_volume_width - volume_up_text.get_width()) // 2, volume_up_button_y + (button_volume_height - volume_up_text.get_height()) // 2))
screen.blit(volume_down_text, (volume_down_button_x + (button_volume_width - volume_down_text.get_width()) // 2, volume_down_button_y + (button_volume_height - volume_down_text.get_height()) // 2))

pygame.mixer.music.load('./src/sound/sound_main.mp3')
pygame.mixer.music.play(-1)

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
            elif volume_up_button_x <= x <= volume_up_button_x + button_volume_width and volume_up_button_y <= y <= volume_up_button_y + button_volume_height:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1, volume + 0.1))
            elif volume_down_button_x <= x <= volume_down_button_x + button_volume_width and volume_down_button_y <= y <= volume_down_button_y + button_volume_height:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0, volume - 0.1))