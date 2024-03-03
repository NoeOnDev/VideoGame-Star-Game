import pygame
import sys
import random
import threading

# render.py

# input.py

# physics.py

# audio.py

# scenes.py

# gui.py
class HomeScreen:
    def __init__(self, win):
        self.win = win
        self.win_width, self.win_height = win.get_size()
        self.background = pygame.image.load('./src/img/home.jpg')
        self.background = pygame.transform.scale(self.background, (self.win_width, self.win_height))
        self.title_font = pygame.font.Font(None, 70)
        self.button_font = pygame.font.Font(None, 50)
        self.title_text = self.title_font.render('Space Game', True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(self.win_width / 2, self.win_height / 2 - 50))
        self.button_width, self.button_height = 200, 50
        self.start_button = pygame.Rect(self.win_width / 2 - self.button_width / 2, self.win_height / 2 + 10, self.button_width, self.button_height)
        self.menu_run = True
    
    def draw(self):
        while self.menu_run:
            self.win.blit(self.background, (0, 0))
            mx, my = pygame.mouse.get_pos()
            self.win.blit(self.title_text, self.title_text_rect)
            pygame.draw.rect(self.win, (0, 255, 0), self.start_button)
            button_text = self.button_font.render('Start', True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=self.start_button.center)
            self.win.blit(button_text, button_text_rect)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            if self.start_button.collidepoint((mx, my)) and click:   
                self.menu_run = False
            pygame.display.update()

# entities.py
class CheckPoint:
    def __init__(self, win):
        self.win = win
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0)
        self.x = self.win.get_width() - self.width - 10
        self.y = self.win.get_height() - self.height - 10

    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 0, 255)
        self.vel = 2

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, checkpoint):
        return (self.x < checkpoint.x + checkpoint.width and
                self.x + self.width > checkpoint.x and
                self.y < checkpoint.y + checkpoint.height and
                self.y + self.height > checkpoint.y)

def relocate_enemies(enemies):
    min_distance = 150 
    for enemy in enemies:
        for other_enemy in enemies:
            if enemy != other_enemy:
                distance = ((enemy.x - other_enemy.x) ** 2 + (enemy.y - other_enemy.y) ** 2) ** 0.5
                if distance < min_distance:
                    enemy.x = random.randint(0, 800)
                    enemy.y = random.randint(0, 500)
                    relocate_enemies(enemies)
                    return


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.vel = 3
        self.direction_x = 1  
        self.direction_y = 1  

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.vel * self.direction_x
        self.y += self.vel * self.direction_y

    def check_boundary_collision(self, window_width, window_height):
        if self.x <= 0 or self.x + self.width >= window_width:
            self.direction_x *= -1
        if self.y <= 0 or self.y + self.height >= window_height:
            self.direction_y *= -1

    def check_enemy_collision(self, enemies):
        for enemy in enemies:
            if enemy != self:
                if (self.x < enemy.x + enemy.width and
                    self.x + self.width > enemy.x and
                    self.y < enemy.y + enemy.height and
                    self.y + self.height > enemy.y):
                    
                    self.direction_x *= -1
                    self.direction_y *= -1
                    enemy.direction_x *= -1
                    enemy.direction_y *= -1
                    break


# main.py
def game_loop(win):
    player_width, player_height = 50, 50
    player_x = 10
    player_y = 10
    player = Player(player_x, player_y)
    checkpoint = CheckPoint(win)

    clock = pygame.time.Clock()
    background = pygame.image.load('./src/img/space.jpg')
    enemies = []
    for i in range(12):
        enemy_x = random.randint(0, win.get_width() - player_width)
        enemy_y = random.randint(0, win.get_height() - player_height)
        while (abs(enemy_x - player_x) < player_width + 20 and abs(enemy_y - player_y) < player_height + 20) or \
              (abs(enemy_x - checkpoint.x) < checkpoint.width + 20 and abs(enemy_y - checkpoint.y) < checkpoint.height + 20):
            enemy_x = random.randint(0, win.get_width() - player_width)
            enemy_y = random.randint(0, win.get_height() - player_height)
        enemy = Enemy(enemy_x, enemy_y)
        enemies.append(enemy)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.vel > 0:
            player.x -= player.vel
        if keys[pygame.K_RIGHT] and player.x + player.vel < win.get_width() - player.width:
            player.x += player.vel
        if keys[pygame.K_UP] and player.y - player.vel > 0:
            player.y -= player.vel
        if keys[pygame.K_DOWN] and player.y + player.vel < win.get_height() - player.height:
            player.y += player.vel
        win.blit(background, (0, 0))

        for enemy in enemies:
            enemy.check_enemy_collision(enemies)

        for enemy in enemies:
            enemy.move()
            enemy.check_boundary_collision(win.get_width(), win.get_height())
            enemy.draw(win)

        player.draw(win)
        checkpoint.draw()

        if player.check_collision(checkpoint):
            run = False

        pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((850, 531))
    home_screen = HomeScreen(win)
    home_screen.draw()

    game_loop(win)

if __name__ == "__main__":
    main()