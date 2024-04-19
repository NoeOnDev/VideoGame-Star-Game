import asyncio
import pickle

class GameServer:
    def __init__(self):
        self.players = {}

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Nueva conexión desde {addr}")

        player_id = len(self.players) + 1
        self.players[player_id] = writer

        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                message = pickle.loads(data)
                print(f"Recibido: {message} de {addr}")

                if 'player_pos' in message:
                    self.players[player_id].write(pickle.dumps({'player_pos': message['player_pos']}))
                    await self.players[player_id].drain()

        finally:
            del self.players[player_id]
            writer.close()
            await writer.wait_closed()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, 'localhost', 8888)

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    game_server = GameServer()
    asyncio.run(game_server.start_server())