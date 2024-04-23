import asyncio
import websockets
import pygame
from pygame.locals import *
import json
import time

server_ip = '44.196.162.180'
server_port = 9009

pygame.init()
screen = pygame.display.set_mode((850, 530))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)

player_state = {'x': 400, 'y': 300, 'ready': False, 'latency': 0}

global_state = {}
meteors = []

remaining_time = 0

winner_message = ''
loser_message = ''

pygame.mixer.init()
current_music = None

waiting_music = pygame.mixer.Sound('./src/sound/sound_main.mp3')
waiting_music.set_volume(0.1)

game_music = pygame.mixer.Sound('./src/sound/sound_play.mp3')
game_music.set_volume(0.1)

background = pygame.image.load('./src/img/space.jpg')
ship_image = pygame.image.load('./src/img/nave.png')
meteor_image = pygame.image.load('./src/img/asteroide.png')

def play_music(music):
    global current_music
    if current_music != music:
        pygame.mixer.stop()
        music.play(-1)
        current_music = music

async def update_state(websocket):
    global global_state, meteors, remaining_time, winner_message, loser_message

    data = await websocket.recv()
    if data:
        state = json.loads(data)
        global_state = state['global_state']
        meteors = state.get('meteors', [])
        remaining_time = state.get('remaining_time', 0)
        everyone_won = state.get('everyone_won', False)
        everyone_lost = state.get('everyone_lost', False)

        if everyone_won:
            winner_message = 'Congratulations, you won!'
        if everyone_lost:
            loser_message = 'Sorry, everyone lost.'

async def send_movement(websocket):
    start_time = time.time()
    await websocket.send(json.dumps(player_state))
    await update_state(websocket)
    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)
    player_state['latency'] = latency_ms

async def main():
    global winner_message, loser_message
    winner_message = ''
    loser_message = ''

    async with websockets.connect(f"ws://{server_ip}:{server_port}") as websocket:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    player_state['ready'] = not player_state['ready']
                    await send_movement(websocket)
            
            keys = pygame.key.get_pressed()
            
            if keys[K_LEFT] and player_state['x'] > 0:
                player_state['x'] -= 5
            if keys[K_RIGHT] and player_state['x'] < 830:
                player_state['x'] += 5
            if keys[K_UP] and player_state['y'] > 0:
                player_state['y'] -= 5
            if keys[K_DOWN] and player_state['y'] < 510:
                player_state['y'] += 5

            await send_movement(websocket)

            screen.blit(background, (0, 0))

            for player_id, pos in global_state.items():
                ship = pygame.transform.scale(ship_image, (35, 20))
                screen.blit(ship, (pos['x'], pos['y']))

                gamertag = font.render(f'Player {player_id}', True, (255, 255, 255))
                screen.blit(gamertag, (pos['x'], pos['y'] - 20))
                
            meteor = pygame.transform.scale(meteor_image, (20, 20))
            for meteor_info in meteors:
                screen.blit(meteor, (int(meteor_info['x']), int(meteor_info['y'])))

            ready_players = sum(1 for player in global_state.values() if 'ready' in player and player['ready'])
            total_players = len(global_state)
            if ready_players < total_players:
                message = f'READY PLAYERS ({ready_players}/{total_players})'
                play_music(waiting_music)
            else:
                message = 'ALL PLAYERS ARE READY!'
                play_music(game_music)

            message_text = font.render(message, True, (255, 255, 255))
            screen.blit(message_text, (10, 10))

            latency_text = font.render(f'{player_state["latency"]} ms', True, (255, 255, 255))
            screen.blit(latency_text, (850 - latency_text.get_width() - 10, 10))

            if remaining_time > 0:
                time_text = font.render(f'Remaining time: {int(remaining_time)} sec', True, (255, 255, 255))
                screen.blit(time_text, (10, 30))

            if winner_message:
                winner_text = font.render(winner_message, True, (255, 255, 255))
                screen.blit(winner_text, (425 - winner_text.get_width() // 2, 265 - winner_text.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                running = False
                
            if loser_message:
                loser_text = font.render(loser_message, True, (255, 255, 255))
                screen.blit(loser_text, (425 - loser_text.get_width() // 2, 265 - loser_text.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                running = False

            pygame.display.update()

            clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())