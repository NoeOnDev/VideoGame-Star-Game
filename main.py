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
    pass

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

    spaceship = pygame.image.load('./src/img/nave.png')
    spaceship_rect = spaceship.get_rect()
    spaceship_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        screen.blit(spaceship, spaceship_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()