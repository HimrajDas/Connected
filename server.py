import socket
import threading
import sys

class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, self.port))
        self.serverSocket.listen()
        self.clients = []
        self.names = []

    def run_server(self):
        while True:
            print("Listening bro....")
            client, address = self.serverSocket.accept()
            print(f"Connected with : {str(address)}")

            name = client.recv(1024).decode(('utf-8'))
            self.names.append(name)
            self.clients.append(client)

            print(f"Name is {name}")
            self.broadcast_msg(f"{name} joined!".encode('utf-8'))
            client.send("Connected to server!".encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(1024)
                if not msg:
                    break
                self.broadcast_msg(msg)
            
            except (ConnectionError, KeyboardInterrupt) as e:
                print(f"Error handling client: {e}")
                client.close()
                if isinstance(e, KeyboardInterrupt):
                    print("Keyboard Interupted!!")
                    self.cleanup()
                    sys.exit()

    
    def broadcast_msg(self, msg):
        for client in self.clients:
            client.send(msg)


    def cleanup(self):
        self.serverSocket.close()


if __name__ == "__main__":
    server = Server("127.0.0.1", 12000)
    try:
        server.run_server()
    except KeyboardInterrupt:
        print("Keyboard interupted!!!")
        server.cleanup()
        sys.exit()