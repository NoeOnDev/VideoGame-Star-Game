import pygame
import pickle
import asyncio

pygame.init()

WIDTH, HEIGHT = 850, 530
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Multijugador")

GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

async def handle_server_events(reader, writer):
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            message = pickle.loads(data)
            print(f"Recibido: {message}")

            if 'player_pos' in message:
                player.rect.x, player.rect.y = message['player_pos']

    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    reader, writer = await asyncio.open_connection('44.196.162.180', 8888)

    server_task = asyncio.create_task(handle_server_events(reader, writer))

    global player
    player = Player()
    players = pygame.sprite.Group()
    players.add(player)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        players.update()

        player_pos = (player.rect.x, player.rect.y)
        writer.write(pickle.dumps({'player_pos': player_pos}))
        await writer.drain()

        screen.fill((0, 0, 0))
        players.draw(screen)
        pygame.display.flip()

    server_task.cancel()
    writer.close()
    await writer.wait_closed()

asyncio.run(main())