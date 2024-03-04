import pygame
import sys
import threading
import random
import time
import queue
import pygame.mixer
from pygame.locals import *

# Constantes
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 531
BASE_WIDTH = 100
BASE_HEIGHT = 100
FPS = 60

# Entidades
class Player:
    def __init__(self, image_path, speed, initial_position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.speed = speed
        self.lives = 3
        
    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            print("¡El jugador ha perdido!")
            return self.lives

    def move(self, keys, window_width, window_height):
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < window_height:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < window_width:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Base:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroid:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 200), random.randint(0, WINDOW_HEIGHT))

    def move(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.reset_position()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
class Enemy:
    def __init__(self, image_path, speed, initial_position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.speed = speed

    def move(self, player_position):
        if self.rect.x < player_position[0]:
            self.rect.x += self.speed
        if self.rect.x > player_position[0]:
            self.rect.x -= self.speed
        if self.rect.y < player_position[1]:
            self.rect.y += self.speed
        if self.rect.y > player_position[1]:
            self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Vistas
class PlayButton:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('./src/img/home.jpg')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.play_button = PlayButton('./src/img/play.png', (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.play_button.draw(self.screen)

    def handle_event(self, event):
        if self.play_button.is_clicked(event):
            return True
        return False

class LoserView:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('./src/img/space.jpg')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.retry_button = PlayButton('./src/img/retry.png', (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.exit_button = PlayButton('./src/img/quit.png', (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.retry_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def handle_event(self, event):
        if self.retry_button.is_clicked(event):
            return 'retry'
        elif self.exit_button.is_clicked(event):
            return 'exit'
        return None
    
# Hilos
class PlayerThread(threading.Thread):
    def __init__(self, player, keys, window_width, window_height):
        super().__init__()
        self.player = player
        self.keys = keys
        self.window_width = window_width
        self.window_height = window_height

    def run(self):
        self.player.move(self.keys, self.window_width, self.window_height)

class EnemyThread(threading.Thread):
    def __init__(self, enemy, player_position):
        super().__init__()
        self.enemy = enemy
        self.player_position = player_position

    def run(self):
        self.enemy.move(self.player_position)

class AsteroidThread(threading.Thread):
    def __init__(self, asteroid):
        super().__init__()
        self.asteroid = asteroid

    def run(self):
        self.asteroid.move()

class MusicThread(threading.Thread):
    def __init__(self, music_file):
        super().__init__()
        self.music_file = music_file

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1) 
        
class PlayerThread(threading.Thread):
    pass

class EnemyThread(threading.Thread):
    pass

class AsteroidThread(threading.Thread):
    pass

class AudioThread(threading.Thread):
    pass

class GraphicsThread(threading.Thread):
    pass

class EnemyAI(threading.Thread):
    pass

# Barreras
start_level_barrier = threading.Barrier(12)
start_music_barrier = threading.Barrier(2)
update_score_barrier = threading.Barrier(2)

# Semáforos
score_semaphore = threading.Semaphore(1)
enemy_list_semaphore = threading.Semaphore(1)
player_position_semaphore = threading.Semaphore(1)

# Eventos
new_level_event = threading.Event()
game_over_event = threading.Event()
shot_fired_event = threading.Event()

def generate_asteroid_y_position():
        return random.randint(0, WINDOW_HEIGHT)

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    menu_music_thread = MusicThread('./src/sound/sound_main.mp3')
    menu_music_thread.start()

    menu_view = MenuView(screen)
    game_started = False

    while not game_started:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            game_started = menu_view.handle_event(event)

        menu_view.draw()
        pygame.display.flip()

    pygame.mixer.music.stop()
    game_music_thread = MusicThread('./src/sound/sound_play.mp3')
    game_music_thread.start()
    
    player = Player('./src/img/nave.png', 1, (20, 20))
    asteroids = [Asteroid('./src/img/asteroide.png', 4) for i in range(9)]
    base = Base('./src/img/base.png', (WINDOW_WIDTH - BASE_WIDTH, WINDOW_HEIGHT - BASE_HEIGHT))

    background = pygame.image.load('./src/img/space.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw(screen)

        for asteroid in asteroids:
            if player.rect.colliderect(asteroid.rect):
                print("¡El jugador ha chocado con un asteroide!")
                if player.lose_life() == 0:
                    loser_view = LoserView(screen)
                    game_over = False
                    while not game_over:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            action = loser_view.handle_event(event)
                            if action == 'retry':
                                main()
                            elif action == 'exit':
                                pygame.quit()
                                sys.exit()
                        loser_view.draw()
                        pygame.display.flip()

        keys = pygame.key.get_pressed()
        player.move(keys, WINDOW_WIDTH, WINDOW_HEIGHT)

        player.draw(screen)
        base.draw(screen)

        if player.rect.colliderect(base.rect):
            print("¡Nivel completado!")
            main()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()