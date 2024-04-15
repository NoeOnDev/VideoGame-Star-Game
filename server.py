import socket
import threading

class Server:
    def __init__(self, host = 'localhost', port = 5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.positions = {}

    def broadcast(self, message, client):
        for c in self.clients:
            if c != client:
                c.send(message)

    def handle(self, client):
        while True:
            try:
                position = client.recv(1024)
                self.positions[client] = position
                self.broadcast(position, client)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                self.broadcast(self.positions[self.clients[index % len(self.clients)]], self.clients[index % len(self.clients)])
                break

    def run(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            print(f'Conexión establecida con {str(addr)}')
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

server = Server()
server.run()