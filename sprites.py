import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ 50, 50])
        self.image.fill(settings.RED)
        self.rect = self.image.get_rect()
        self.rect.center = (settings.window_size[0] // 2, settings.window_size[1] // 2)
    
    def update(self):
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
