import pygame
import sys
import threading
import queue
from pygame.locals import *

# Constantes
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 531
FPS = 60

# Entidades
class Player:
    def __init__(self, image_path, speed, initial_position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.speed = speed

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

class Asteroid:
    pass

class Enemy:
    pass

# Vistas
class GameView:
    pass

# Hilos
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

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    player = Player('./src/img/nave.png', 3, (WINDOW_WIDTH // 20, WINDOW_HEIGHT // 20))

    background = pygame.image.load('./src/img/space.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys, WINDOW_WIDTH, WINDOW_HEIGHT)

        screen.blit(background, (0, 0))

        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()