import pygame

# main.py
def main ():
    pygame.init()

if __name__ == "__main__":
    main()

# entities.py
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 50
        self.height = 50
        self.color = (0, 0, 255)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
# render.py

# input.py

# physics.py

# audio.py

# gui.py

# scenes.py