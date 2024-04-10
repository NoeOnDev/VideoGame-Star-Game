import pygame
import sys
import random

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

def start_game():
    game_window_width = 850
    game_window_height = 531
    game_screen = pygame.display.set_mode((game_window_width, game_window_height))
    pygame.display.set_caption("My Star - Game")

    clock = pygame.time.Clock()

    background_image = pygame.image.load('./src/img/space.jpg')
    background_image = pygame.transform.scale(background_image, (game_window_width, game_window_height))

    base_image = pygame.image.load('./src/img/base.png')
    base_width = 76
    base_height = 71
    base_image = pygame.transform.scale(base_image, (base_width, base_height))
    base_x = game_window_width - base_width
    base_y = game_window_height - base_height
    base_mask = pygame.mask.from_surface(base_image)

    player_image = pygame.image.load('./src/img/nave.png')
    player_width = 40
    player_height = 25
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
    player_x = 0
    player_y = (game_window_height - player_height) / 2
    player_mask = pygame.mask.from_surface(player_image)

    meteor_sizes = [(50, 50), (30, 30), (70, 70)]
    meteors = []
    for size in meteor_sizes:
        meteor_image = pygame.image.load('./src/img/asteroide.png')
        meteor_image = pygame.transform.scale(meteor_image, size)
        meteor_x = game_window_width - size[0]
        meteor_y = random.randint(0, game_window_height - size[1])
        meteor_mask = pygame.mask.from_surface(meteor_image)
        meteors.append({
            'image': meteor_image,
            'x': meteor_x,
            'y': meteor_y,
            'mask': meteor_mask,
            'width': size[0],
            'height': size[1]
        })

    player_speed = 1
    move_left = move_right = move_up = move_down = False

    meteor_speed = 2

    while True:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_UP:
                    move_up = True
                elif event.key == pygame.K_DOWN:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_UP:
                    move_up = False
                elif event.key == pygame.K_DOWN:
                    move_down = False

        if move_left and player_x - player_speed > 0:
            player_x -= player_speed
        if move_right and player_x + player_speed < game_window_width - player_width:
            player_x += player_speed
        if move_up and player_y - player_speed > 0:
            player_y -= player_speed
        if move_down and player_y + player_speed < game_window_height - player_height:
            player_y += player_speed

        for meteor in meteors:
            meteor['x'] -= meteor_speed
            if meteor['x'] + meteor['width'] < 0:
                meteor['x'] = game_window_width
                meteor['y'] = random.randint(0, game_window_height - meteor['height'])

        game_screen.blit(background_image, (0, 0))
        game_screen.blit(base_image, (base_x, base_y))
        game_screen.blit(player_image, (player_x, player_y))
        for meteor in meteors:
            game_screen.blit(meteor['image'], (meteor['x'], meteor['y']))

        offset_x_base = base_x - player_x
        offset_y_base = base_y - player_y

        if player_mask.overlap(base_mask, (offset_x_base, offset_y_base)):
            print("Fin del juego")
            pygame.quit()
            sys.exit()

        for meteor in meteors:
            offset_x_meteor = meteor['x'] - player_x
            offset_y_meteor = meteor['y'] - player_y
            if player_mask.overlap(meteor['mask'], (offset_x_meteor, offset_y_meteor)):
                print("Perdiste")
                # pygame.quit()
                #sys.exit()

        pygame.display.flip()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if start_button_x <= x <= start_button_x + button_width and start_button_y <= y <= start_button_y + button_height:
                print("Iniciar juego")
                pygame.mixer.music.stop()
                start_game()
            elif config_button_x <= x <= config_button_x + button_width and config_button_y <= y <= config_button_y + button_height:
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