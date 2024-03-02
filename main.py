import pygame
import sys

# entities.py
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 50
        self.height = 50
        self.color = (0, 0, 255)
        self.vel = 3
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

# main.py
def main_menu(win):
    menu_run = True
    title_font = pygame.font.Font(None, 70)
    button_font = pygame.font.Font(None, 50)
    title_text = title_font.render('Space', True, (255, 255, 255))
    start_button = pygame.Rect(350, 250, 200, 50)

    while menu_run:
        win.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()

        win.blit(title_text, (325, 100))

        pygame.draw.rect(win, (0, 255, 0), start_button)  # Dibuja un botón verde
        button_text = button_font.render('Start', True, (255, 255, 255))
        win.blit(button_text, (start_button.x + 50, start_button.y + 10))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        if start_button.collidepoint((mx, my)) and click:
            menu_run = False

        pygame.display.update()
        
def main(win):
    pygame.init()
    
    player = Player()
    clock = pygame.time.Clock()
    background = pygame.image.load('./src/img/space.jpg')
    
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.vel > 0:
            player.x -= player.vel
        if keys[pygame.K_RIGHT] and player.x + player.vel < 850 - player.width:
            player.x += player.vel
        if keys[pygame.K_UP] and player.y - player.vel > 0:
            player.y -= player.vel
        if keys[pygame.K_DOWN] and player.y + player.vel < 531 - player.height:
            player.y += player.vel
        
        win.blit(background, (0, 0))
        player.draw(win)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((850, 531))
    main_menu(win)
    main(win)

# render.py

# input.py

# physics.py

# audio.py

# gui.py

# scenes.py