import pygame

class GameWindow:
    def __init__(self, width, height, background_image_path, corner_image_path):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = MySprite(background_image_path)
        self.corner_image = MySprite(corner_image_path)

    def render(self):
        self.screen.blit(self.background.image, (0, 0))
        corner_image_width = self.corner_image.image.get_width()
        corner_image_height = self.corner_image.image.get_height()
        self.screen.blit(self.corner_image.image, (self.width - corner_image_width, self.height - corner_image_height))
        pygame.display.set_caption("My Star - Game")
        pygame.display.flip()

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

class Game:
    def check_collision(self, sprite1, sprite2):
        offset_x = sprite2.rect.x - sprite1.rect.x
        offset_y = sprite2.rect.y - sprite1.rect.y
        return sprite1.mask.overlap(sprite2.mask, (offset_x, offset_y)) is not None