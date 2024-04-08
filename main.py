import pygame
import sys
from game import GameWindow
from game import Game

pygame.init()
pygame.mixer.init()

window_main_width = 800
window_main_height = 470

screen = pygame.display.set_mode((window_main_width, window_main_height))

pygame.display.set_caption("My Star - Home")

background = pygame.image.load('./src/img/home.jpg')

volume_up_image = pygame.image.load('./src/img/volume_up.png')
volume_down_image = pygame.image.load('./src/img/volume_down.png')
mute_image = pygame.image.load('./src/img/mute.png')

start_button_color = (0, 255, 19)
config_button_color = (109, 109, 255)
exit_button_color = (255, 0, 0)
volume_up_button_color = (255, 255, 0)
volume_down_button_color = (255, 0, 0)
mute_button_color = (255, 0, 0)
border_color = (23, 23, 23)

button_width = 180
button_height = 60
button_volume_width = 40
button_volume_height = 40
border_width = 5

start_button_x = window_main_width / 2 - button_width / 2
start_button_y = window_main_height / 2 - button_height / 2 - 30

exit_button_x = window_main_width / 2 - button_width / 2
exit_button_y = start_button_y + button_height + 90

config_button_x = window_main_width / 2 - button_width / 2
config_button_y = (start_button_y + exit_button_y) / 2 - button_height + 60

volume_up_button_x = 0
volume_up_button_y = window_main_height - 3 * button_volume_height -10

volume_down_button_x = 0
volume_down_button_y = window_main_height - 2 * button_volume_height -5

mute_button_x = 0
mute_button_y = window_main_height - button_volume_height

screen.blit(background, (0, 0))

pygame.draw.rect(screen, border_color, pygame.Rect(start_button_x - border_width, start_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(config_button_x - border_width, config_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, config_button_color, pygame.Rect(config_button_x, config_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(exit_button_x - border_width, exit_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(volume_up_button_x - border_width, volume_up_button_y - border_width, button_volume_width + 2 * border_width, button_volume_height + 2 * border_width))
pygame.draw.rect(screen, volume_up_button_color, pygame.Rect(volume_up_button_x, volume_up_button_y, button_volume_width, button_volume_height))

pygame.draw.rect(screen, border_color, pygame.Rect(volume_down_button_x - border_width, volume_down_button_y - border_width, button_volume_width + 2 * border_width, button_volume_height + 2 * border_width))
pygame.draw.rect(screen, volume_down_button_color, pygame.Rect(volume_down_button_x, volume_down_button_y, button_volume_width, button_volume_height))

pygame.draw.rect(screen, border_color, pygame.Rect(mute_button_x - border_width, mute_button_y - border_width, button_volume_width + 2 * border_width, button_volume_height + 2 * border_width))
pygame.draw.rect(screen, mute_button_color, pygame.Rect(mute_button_x, mute_button_y, button_volume_width, button_volume_height))

font = pygame.font.Font(None, 40)

start_text = font.render('Play', True, (0, 0, 0))
exit_text = font.render('Exit', True, (0, 0, 0))
config_text = font.render('Config', True, (0, 0, 0))

volume_up_image = pygame.transform.scale(volume_up_image, (button_volume_width, button_volume_height))
volume_down_image = pygame.transform.scale(volume_down_image, (button_volume_width, button_volume_height))
mute_image = pygame.transform.scale(mute_image, (button_volume_width, button_volume_height))
game_name_font = pygame.font.Font(None, 72)
game_name_text = game_name_font.render('My Star Game', True, (255, 255, 255))
game_name_x = window_main_width / 2 - game_name_text.get_width() / 2
game_name_y = start_button_y / 2 - game_name_text.get_height() / 2

screen.blit(game_name_text, (game_name_x, game_name_y))
screen.blit(start_text, (start_button_x + (button_width - start_text.get_width()) // 2, start_button_y + (button_height - start_text.get_height()) // 2))
screen.blit(exit_text, (exit_button_x + (button_width - exit_text.get_width()) // 2, exit_button_y + (button_height - exit_text.get_height()) // 2))
screen.blit(config_text, (config_button_x + (button_width - config_text.get_width()) // 2, config_button_y + (button_height - config_text.get_height()) // 2))
screen.blit(volume_up_image, (volume_up_button_x, volume_up_button_y))
screen.blit(volume_down_image, (volume_down_button_x, volume_down_button_y))
screen.blit(mute_image, (mute_button_x, mute_button_y))

# Deshabilitado mientras desarrollo el juego
# pygame.mixer.music.load('./src/sound/sound_main.mp3')
# pygame.mixer.music.play(-1)

pygame.display.flip()

game = Game()
game_window = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if start_button_x <= x <= start_button_x + button_width and start_button_y <= y <= start_button_y + button_height:
                print("Iniciar juego")
                pygame.mixer.music.stop()
                game_window = GameWindow(850, 531, './src/img/space.jpg', './src/img/base.png', './src/img/nave.png')
                game_window.render()

            if config_button_x <= x <= config_button_x + button_width and config_button_y <= y <= config_button_y + button_height:
                print("Configuración")
            elif exit_button_x <= x <= exit_button_x + button_width and exit_button_y <= y <= exit_button_y + button_height:
                print("Salir")
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif volume_up_button_x <= x <= volume_up_button_x + button_volume_width and volume_up_button_y <= y <= volume_up_button_y + button_volume_height:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1, volume + 0.1))
            elif volume_down_button_x <= x <= volume_down_button_x + button_volume_width and volume_down_button_y <= y <= volume_down_button_y + button_volume_height:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0, volume - 0.1))
            elif mute_button_x <= x <= mute_button_x + button_volume_width and mute_button_y <= y <= mute_button_y + button_volume_height:
                pygame.mixer.music.set_volume(0)