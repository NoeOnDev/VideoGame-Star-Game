import pygame

class GameWindow:
    def __init__(self, width, height, background_image_path, corner_image_path):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load(background_image_path)
        self.corner_image = pygame.image.load(corner_image_path)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        corner_image_width = self.corner_image.get_width()
        corner_image_height = self.corner_image.get_height()
        self.screen.blit(self.corner_image, (self.width - corner_image_width, self.height - corner_image_height))
        pygame.display.set_caption("My Star - Game")
        pygame.display.flip()