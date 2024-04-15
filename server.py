import socket
import threading

class Server:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.positions = {}

    def broadcast(self, message, client):
        for c in self.clients:
            if c != client:
                try:
                    c.send(message)
                except BrokenPipeError:
                    print(f"Error enviando mensaje a un cliente. Cliente desconectado.")
                    c.close()
                    self.clients.remove(c)

    def handle(self, client):
        while True:
            try:
                position = client.recv(1024)
                if not position:
                    print(f"Cliente {client} se ha desconectado.")
                    self.clients.remove(client)
                    client.close()
                    break
                
                self.positions[client] = position
                print(f"Recibida posición de cliente: {position.decode()}")
                self.broadcast(position, client)
            except Exception as e:
                print(f"Error manejando cliente {client}: {e}")
                self.clients.remove(client)
                client.close()
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
