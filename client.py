import pygame
import pickle
import asyncio

pygame.init()

WIDTH, HEIGHT = 850, 530
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Multijugador")

GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, keys):
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

async def handle_server_events(reader, writer, players):
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            message = pickle.loads(data)
            print(f"Recibido: {message}")

            if 'players' in message:
                for player_data in message['players']:
                    player_id = player_data['id']
                    player_pos = player_data['pos']
                    if player_id not in players:
                        players[player_id] = Player(*player_pos)
                    else:
                        players[player_id].rect.x, players[player_id].rect.y = player_pos

    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    reader, writer = await asyncio.open_connection('44.196.162.180', 8888)

    player = Player(WIDTH // 2, HEIGHT // 2)
    players = {1: player}

    server_task = asyncio.create_task(handle_server_events(reader, writer, players))

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        player_pos = (player.rect.x, player.rect.y)
        writer.write(pickle.dumps({'player_pos': player_pos}))
        await writer.drain()

        screen.fill((0, 0, 0))
        for player in players.values():
            screen.blit(player.image, player.rect)
        pygame.display.flip()

    server_task.cancel()
    writer.close()
    await writer.wait_closed()

asyncio.run(main())