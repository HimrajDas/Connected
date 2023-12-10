import socket
import threading
import sys
import logging

logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        self.clients = []
        self.names = []

    def run_server(self):
        while True:
            logger.info("Listening for connections...")
            client, address = self.server_socket.accept()
            logger.info(f"Client connected from {address}")

            try:
                name = client.recv(1024).decode("utf-8")
                logger.info(f"Client name: {name}")

                self.names.append(name)
                self.clients.append(client)

                self.broadcast_message(f"{name} joined!".encode("utf-8"))
                client.send("Connected to server!".encode("utf-8"))

                threading.Thread(target=self.handle_client, args=(client,)).start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")
                client.close()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)

                if not message:
                    break

                self.broadcast_message(message)
            except ConnectionError:
                logger.error(f"Connection error with client: {sys.exc_info()}")
                client.close()
                break

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")

    def cleanup(self):
        logger.info("Closing connections...")
        self.server_socket.close()
        # for client in self.clients:
        #     client.close()


if __name__ == "__main__":
    try:
        server = Server("127.0.0.1", 12000)
        server.run_server()
    except KeyboardInterrupt:
        logger.info("Server stopped.")
        server.cleanup()
        sys.exit()
