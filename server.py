import asyncio
import websockets
import json
import random

server_ip = '0.0.0.0'
server_port = 9009

clients = set()

global_state = {}

player_counter = 0

meteors = []

all_ready = False
all_won = False
all_lost = False

remaining_time = 0

def check_all_ready():
    global all_ready
    all_ready = all(player['ready'] for player in global_state.values())

async def generate_meteors():
    interval = 1

    while True:
        if clients and all_ready and remaining_time > 0:
            num_meteors = random.choice([0, 0.5, 1])

            for _ in range(int(num_meteors)):
                meteor = {
                    'x': 850,
                    'y': random.randint(0, 530),
                    'velocity_x': random.uniform(-2, -5),
                    'velocity_y': 0
                }
                meteors.append(meteor)
        
        await asyncio.sleep(interval)

async def handle_client(websocket, path):
    global player_counter, remaining_time
    player_id = player_counter
    player_counter += 1
    global_state[player_id] = {'x': 400, 'y': 300, 'ready': False}
    clients.add(websocket)
    print(f"Player {player_id} has joined the server.")

    try:
        while True:
            data = await websocket.recv()
            movement = json.loads(data)
            global_state[player_id] = movement
            
            if not movement['ready'] and remaining_time > 0:
                remaining_time = 0
                meteors.clear()

    except websockets.ConnectionClosed:
        print(f"Connection with client {player_id} has been unexpectedly closed.")
    finally:
        clients.remove(websocket)
        if player_id in global_state:
            del global_state[player_id]
            print(f"Player {player_id} has been removed.")

def check_collisions():
    global remaining_time, all_won, all_lost
    for player_id, player in global_state.items():
        x_player = player['x']
        y_player = player['y']
        
        for meteor in meteors:
            x_meteor = meteor['x']
            y_meteor = meteor['y']
            
            if (x_player - x_meteor) ** 2 + (y_player - y_meteor) ** 2 < 400:
                remaining_time = 0
                all_lost = True
                return
            
        if remaining_time <= 0:
            all_won = True

async def update_state():
    global remaining_time, all_won, all_lost

    while True:
        check_all_ready()

        if all_ready and remaining_time == 0:
            remaining_time = 120
            asyncio.create_task(generate_meteors())
            all_won = False
            all_lost = False
        
        if all_won or all_lost:
            remaining_time = 0
            meteors.clear()
            all_won = False
            all_lost = False
        
        if all_ready and remaining_time > 0:
            remaining_time -= 0.1
            check_collisions()

            if remaining_time <= 0:
                remaining_time = 0
                meteors.clear()
        
        for meteor in meteors:
            meteor['x'] += meteor['velocity_x']
            meteor['y'] += meteor['velocity_y']

        meteors[:] = [meteor for meteor in meteors if meteor['x'] > 0]

        state = {
            'global_state': global_state,
            'meteors': meteors,
            'remaining_time': remaining_time,
            'all_won': all_won,
            'all_lost': all_lost
        }

        state_json = json.dumps(state)
        
        if clients:
            tasks = [asyncio.create_task(client.send(state_json)) for client in clients if client.open]
            if tasks:
                await asyncio.wait(tasks)

        await asyncio.sleep(0.1)

start_server = websockets.serve(handle_client, server_ip, server_port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(update_state())
loop.run_forever()
