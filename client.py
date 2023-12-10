import socket
import sys
import threading
import logging

class Client:
    def __init__(self, ip: str, port: int, username: str):
        self.ip = ip
        self.port = port
        self.username = username.encode('utf-8')

        # Configure logging
        logging.basicConfig(filename="client.log", level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)

        # Create the socket
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.clientSocket.connect((self.ip, self.port))
            self.logger.info("Connected to server.")
        except Exception as e:
            self.logger.error(f"Failed to connect to server: {str(e)}")
            sys.exit(1)

    def write(self):
        while True:
            try:
                msg = f"{self.username.decode('utf-8')}: {input(' ')}"
                self.clientSocket.send(msg.encode('utf-8'))
            except KeyboardInterrupt:
                self.logger.info("Exiting...")
                break
            except Exception as e:
                self.logger.error(f"An error occurred while writing: {str(e)}")
                break

    def read(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode('utf-8')
                self.logger.info(f"Received message: {msg}")
                print(msg)
            except Exception as e:
                self.logger.error(f"An error occurred while reading: {str(e)}")
                self.clientSocket.close()
                break

    def start(self):
        self.connect()

        read_thread = threading.Thread(target=self.read)
        write_thread = threading.Thread(target=self.write)

        read_thread.start()
        write_thread.start()

        read_thread.join()
        write_thread.join()

if __name__ == "__main__":
    try:
        username = input("Enter your name: ").lower()
        client = Client("127.0.0.1", 12000, username)
        client.start()
    except KeyboardInterrupt:
        print("Keyboard interrupted!!!")
        sys.exit(1)
