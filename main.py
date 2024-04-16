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
multiplayer_button_color = (81, 226, 255)
config_button_color = (109, 109, 255)
exit_button_color = (255, 0, 0)
volume_up_button_color = (255, 255, 0)
volume_down_button_color = (255, 0, 0)
mute_button_color = (255, 0, 0)
border_color = (23, 23, 23)

button_width = 180
button_height = 55
button_volume_width = 40
button_volume_height = 40
border_width = 5

start_button_x = window_main_width / 2 - button_width / 2
start_button_y = window_main_height / 2 - button_height / 2 - 50

multiplayer_button_x = window_main_width / 2 - button_width / 2
multiplayer_button_y = start_button_y + button_height + 10

exit_button_x = window_main_width / 2 - button_width / 2
exit_button_y = start_button_y + button_height + 133

config_button_x = window_main_width / 2 - button_width / 2
config_button_y = (start_button_y + exit_button_y) / 2 - button_height + 90

screen.blit(background, (0, 0))

pygame.draw.rect(screen, border_color, pygame.Rect(start_button_x - border_width, start_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(config_button_x - border_width, config_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, config_button_color, pygame.Rect(config_button_x, config_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(exit_button_x - border_width, exit_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))

pygame.draw.rect(screen, border_color, pygame.Rect(multiplayer_button_x - border_width, multiplayer_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
pygame.draw.rect(screen, multiplayer_button_color, pygame.Rect(multiplayer_button_x, multiplayer_button_y, button_width, button_height))

font = pygame.font.Font(None, 40)

start_text = font.render('Play', True, (0, 0, 0))
exit_text = font.render('Exit', True, (0, 0, 0))
config_text = font.render('Settings', True, (0, 0, 0))
multiplayer_text = font.render('Multiplayer', True, (0, 0, 0))

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
screen.blit(multiplayer_text, (multiplayer_button_x + (button_width - multiplayer_text.get_width()) // 2, multiplayer_button_y + (button_height - multiplayer_text.get_height()) // 2))

# Deshabilitado mientras desarrollo el juego
# pygame.mixer.music.load('./src/sound/sound_main.mp3')
# pygame.mixer.music.play(-1)

pygame.display.flip()

def draw_main_home():
    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, border_color, pygame.Rect(start_button_x - border_width, start_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
    pygame.draw.rect(screen, start_button_color, pygame.Rect(start_button_x, start_button_y, button_width, button_height))

    pygame.draw.rect(screen, border_color, pygame.Rect(config_button_x - border_width, config_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
    pygame.draw.rect(screen, config_button_color, pygame.Rect(config_button_x, config_button_y, button_width, button_height))

    pygame.draw.rect(screen, border_color, pygame.Rect(exit_button_x - border_width, exit_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
    pygame.draw.rect(screen, exit_button_color, pygame.Rect(exit_button_x, exit_button_y, button_width, button_height))
    
    pygame.draw.rect(screen, border_color, pygame.Rect(multiplayer_button_x - border_width, multiplayer_button_y - border_width, button_width + 2 * border_width, button_height + 2 * border_width))
    pygame.draw.rect(screen, multiplayer_button_color, pygame.Rect(multiplayer_button_x, multiplayer_button_y, button_width, button_height))

    screen.blit(game_name_text, (game_name_x, game_name_y))
    screen.blit(start_text, (start_button_x + (button_width - start_text.get_width()) // 2, start_button_y + (button_height - start_text.get_height()) // 2))
    screen.blit(exit_text, (exit_button_x + (button_width - exit_text.get_width()) // 2, exit_button_y + (button_height - exit_text.get_height()) // 2))
    screen.blit(config_text, (config_button_x + (button_width - config_text.get_width()) // 2, config_button_y + (button_height - config_text.get_height()) // 2))
    screen.blit(multiplayer_text, (multiplayer_button_x + (button_width - multiplayer_text.get_width()) // 2, multiplayer_button_y + (button_height - multiplayer_text.get_height()) // 2))
    
    pygame.display.flip()

is_modal_open = False
volume_up_button = None
volume_down_button = None
mute_button = None
close_button = None

def draw_modal_home():
    global is_modal_open, volume_up_button, volume_down_button, mute_button, close_button
    is_modal_open = True
    modal_width = 500
    modal_height = 400
    modal_x = (window_main_width - modal_width) / 2
    modal_y = (window_main_height - modal_height) / 2
    
    modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    pygame.draw.rect(screen, (255, 255, 255), modal_rect)
    pygame.draw.rect(screen, (0, 0, 0), modal_rect, 5)

    font = pygame.font.Font(None, 40)
    title_text = font.render("Settings", True, (0, 0, 0))
    title_text_x = modal_x + (modal_width - title_text.get_width()) / 2
    title_text_y = modal_y + 20
    screen.blit(title_text, (title_text_x, title_text_y))
    
    volume_text = font.render("Volume", True, (0, 0, 0))
    volume_text_x = modal_x + 20
    volume_text_y = modal_y + 100
    screen.blit(volume_text, (volume_text_x, volume_text_y))

    volume = pygame.mixer.music.get_volume()
    volume_text = font.render(str(int(volume * 100)), True, (0, 0, 0))
    volume_text_x = modal_x + modal_width - 20 - volume_text.get_width()
    volume_text_y = modal_y + 100
    screen.blit(volume_text, (volume_text_x, volume_text_y))
    
    volume_up_button = pygame.Rect(modal_x + modal_width - 60, modal_y + 100, 40, 40)
    volume_down_button = pygame.Rect(modal_x + modal_width - 60, modal_y + 150, 40, 40)
    mute_button = pygame.Rect(modal_x + modal_width - 60, modal_y + 200, 40, 40)
    
    close_button = pygame.Rect(modal_x + modal_width - 60, modal_y + 20, 40, 40)
    pygame.draw.rect(screen, (255, 255, 255), close_button)
    
    close_image = pygame.image.load('./src/img/close.png')
    close_image = pygame.transform.scale(close_image, (40, 40))
    screen.blit(close_image, (modal_x + modal_width - 55, modal_y + 12))
    
    pygame.draw.rect(screen, (255, 255, 255), volume_up_button)
    pygame.draw.rect(screen, (255, 255, 255), volume_down_button)
    pygame.draw.rect(screen, (255, 255, 255), mute_button)
    
    volume_up_image = pygame.image.load('./src/img/volume_up.png')
    volume_down_image = pygame.image.load('./src/img/volume_down.png')
    mute_image = pygame.image.load('./src/img/mute.png')

    volume_up_image = pygame.transform.scale(volume_up_image, (40, 40))
    volume_down_image = pygame.transform.scale(volume_down_image, (40, 40))
    mute_image = pygame.transform.scale(mute_image, (40, 40))
    
    screen.blit(volume_up_image, (modal_x + modal_width - 60, modal_y + 100))
    screen.blit(volume_down_image, (modal_x + modal_width - 60, modal_y + 150))
    screen.blit(mute_image, (modal_x + modal_width - 60, modal_y + 200))
    
    pygame.display.flip()

def start_game():
    pygame.init()
    pygame.font.init()
    game_window_width = 850
    game_window_height = 531
    game_screen = pygame.display.set_mode((game_window_width, game_window_height))
    pygame.display.set_caption("My Star - Game")
    
    font = pygame.font.Font(None, 24)
    player_name = "Player 1"
    text = font.render(player_name, True, (255, 255, 255))

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
    for _ in range(random.randint(24, 26)):
        size = random.choice(meteor_sizes)
        meteor_image = pygame.image.load('./src/img/asteroide.png')
        meteor_image = pygame.transform.scale(meteor_image, size)
        meteor_x = random.randint(game_window_width // 2, game_window_width - size[0])
        meteor_y = random.randint(0, game_window_height - size[1])
        meteor_mask = pygame.mask.from_surface(meteor_image)
        meteor_speed = random.randint(1, 3)
        meteors.append({
            'image': meteor_image,
            'x': meteor_x,
            'y': meteor_y,
            'mask': meteor_mask,
            'width': size[0],
            'height': size[1],
            'speed': meteor_speed
        })

    player_speed = 1
    move_left = move_right = move_up = move_down = False
    
    def show_game_over_modal():
        pygame.font.init()
        font = pygame.font.Font(None, 52) 
        button_font = pygame.font.Font(None, 40)

        modal_width = 500
        modal_height = 200
        modal_x = (game_window_width - modal_width) / 2
        modal_y = (game_window_height - modal_height) / 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)

        button_width = 100
        button_height = 100
        button_y = modal_y + 100
        button_spacing = 60

        retry_button = pygame.Rect(modal_x + button_spacing, button_y, button_width, button_height)
        menu_button = pygame.Rect(modal_x + button_width + 2 * button_spacing, button_y, button_width, button_height)
        quit_button = pygame.Rect(modal_x + 2 * button_width + 3 * button_spacing, button_y, button_width, button_height)

        retry_text = button_font.render("Retry", True, (0, 0, 0))
        menu_text = button_font.render("Home", True, (0, 0, 0))
        quit_text = button_font.render("Exit", True, (0, 0, 0))

        game_over_text = font.render("Perdiste", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(game_window_width/2, modal_y + 30))

        blur_surface = pygame.Surface((game_window_width, game_window_height), pygame.SRCALPHA)
        pygame.draw.rect(blur_surface, (231, 83, 83, 50), modal_rect, border_radius=15)
        pygame.draw.rect(blur_surface, (231, 83, 83, 50), retry_button)
        pygame.draw.rect(blur_surface, (231, 83, 83, 50), menu_button)
        pygame.draw.rect(blur_surface, (231, 83, 83, 50), quit_button)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        start_game()
                    elif menu_button.collidepoint(event.pos):
                        draw_main_home()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            game_screen.blit(blur_surface, (0, 0))

            game_screen.blit(retry_text, retry_button.move(10, 10))
            game_screen.blit(menu_text, menu_button.move(10, 10))
            game_screen.blit(quit_text, quit_button.move(10, 10))

            game_screen.blit(game_over_text, game_over_text_rect)
            pygame.display.flip()
    
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
            meteor['x'] -= meteor['speed']
            if meteor['x'] + meteor['width'] < 0:
                meteor['x'] = game_window_width
                meteor['y'] = random.randint(0, game_window_height - meteor['height'])

        game_screen.blit(background_image, (0, 0))
        game_screen.blit(base_image, (base_x, base_y))
        game_screen.blit(player_image, (player_x, player_y))
        game_screen.blit(text, (player_x, player_y - 24))
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
                show_game_over_modal()

        pygame.display.flip()
        
def start_game_muliplayer():
    pygame.init()
    pygame.font.init()
    game_window_width = 850
    game_window_height = 531
    game_screen = pygame.display.set_mode((game_window_width, game_window_height))
    pygame.display.set_caption("My Star - Game")
    
    font = pygame.font.Font(None, 24)
    player_name = "Player"
    text = font.render(player_name, True, (255, 255, 255))

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
    for _ in range(random.randint(24, 26)):
        size = random.choice(meteor_sizes)
        meteor_image = pygame.image.load('./src/img/asteroide.png')
        meteor_image = pygame.transform.scale(meteor_image, size)
        meteor_x = random.randint(game_window_width // 2, game_window_width - size[0])
        meteor_y = random.randint(0, game_window_height - size[1])
        meteor_mask = pygame.mask.from_surface(meteor_image)
        meteor_speed = random.randint(1, 3)
        meteors.append({
            'image': meteor_image,
            'x': meteor_x,
            'y': meteor_y,
            'mask': meteor_mask,
            'width': size[0],
            'height': size[1],
            'speed': meteor_speed
        })

    player_speed = 1
    move_left = move_right = move_up = move_down = False

    start_button = pygame.Rect(game_window_width // 2 - 50, game_window_height // 2 - 25, 100, 50)
    start_button_text = font.render('Inicializar', True, (0, 0, 0))
    text_width, text_height = start_button_text.get_size()

    text_x = start_button.x + (start_button.width - text_width) // 2
    text_y = start_button.y + (start_button.height - text_height) // 2
    game_started = False
    
    initial_player_x = 0
    initial_player_y = (game_window_height - player_height) / 2

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    player_x = initial_player_x
                    player_y = initial_player_y

        if move_left and player_x - player_speed > 0:
            player_x -= player_speed
        if move_right and player_x + player_speed < game_window_width - player_width:
            player_x += player_speed
        if move_up and player_y - player_speed > 0:
            player_y -= player_speed
        if move_down and player_y + player_speed < game_window_height - player_height:
            player_y += player_speed

        if game_started:
            for meteor in meteors:
                meteor['x'] -= meteor['speed']
                if meteor['x'] + meteor['width'] < 0:
                    meteor['x'] = game_window_width
                    meteor['y'] = random.randint(0, game_window_height - meteor['height'])
        
        offset_x_base = base_x - player_x
        offset_y_base = base_y - player_y
        
        game_screen.blit(background_image, (0, 0))
        game_screen.blit(base_image, (base_x, base_y))
        game_screen.blit(player_image, (player_x, player_y))
        game_screen.blit(text, (player_x, player_y - 24))
        
        for meteor in meteors:
            game_screen.blit(meteor['image'], (meteor['x'], meteor['y']))

        if not game_started:
            pygame.draw.rect(game_screen, (255, 255, 255), start_button)
            game_screen.blit(start_button_text, (text_x, text_y))

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
                # show_game_over_modal_multiplayer()
                pass

        pygame.display.flip()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if is_modal_open:
                if volume_up_button.collidepoint(x, y):
                    volume = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(min(1, volume + 0.1))
                elif volume_down_button.collidepoint(x, y):
                    volume = pygame.mixer.music.get_volume()
                    pygame.mixer.music.set_volume(max(0, volume - 0.1))
                elif mute_button.collidepoint(x, y):
                    pygame.mixer.music.set_volume(0)
                elif close_button.collidepoint(x, y):
                    is_modal_open = False
                    draw_main_home()
            else:
                if start_button_x <= x <= start_button_x + button_width and start_button_y <= y <= start_button_y + button_height:
                    print("Iniciar juego")
                    pygame.mixer.music.stop()
                    start_game()
                elif multiplayer_button_x <= x <= multiplayer_button_x + button_width and multiplayer_button_y <= y <= multiplayer_button_y + button_height:
                    print("Multijugador")
                    start_game_muliplayer()
                elif config_button_x <= x <= config_button_x + button_width and config_button_y <= y <= config_button_y + button_height:
                    print("Configuración")
                    draw_modal_home()
                elif exit_button_x <= x <= exit_button_x + button_width and exit_button_y <= y <= exit_button_y + button_height:
                    print("Salir")
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()