import asyncio
import pickle

class GameServer:
    def __init__(self):
        self.players = {}

    async def handle_client(self, reader, writer):
        WIDTH = 850
        HEIGHT = 530
        addr = writer.get_extra_info('peername')
        print(f"Nueva conexión desde {addr}")

        player_id = len(self.players) + 1
        self.players[player_id] = {
            'writer': writer,
            'pos': (WIDTH // 2, HEIGHT // 2)
        }

        try:
            while True:
                try:
                    data = await reader.read(4096)
                except ConnectionResetError:
                    print(f"Conexión cerrada por {addr}")
                    break

                if not data:
                    break
                message = pickle.loads(data)
                print(f"Recibido: {message} de {addr}")

                if 'player_pos' in message:
                    self.players[player_id]['pos'] = message['player_pos']

                    all_players_data = [{'id': id, 'pos': player['pos']} for id, player in self.players.items()]
                    for player in self.players.values():
                        player['writer'].write(pickle.dumps({'players': all_players_data}))
                        await player['writer'].drain()

        finally:
            del self.players[player_id]
            writer.close()
            try:
                await writer.wait_closed()
            except ConnectionResetError:
                print(f"Conexión cerrada por {addr}")

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, '0.0.0.0', 8888)

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    game_server = GameServer()
    asyncio.run(game_server.start_server())