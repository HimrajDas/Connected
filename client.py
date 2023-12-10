import socket
import sys
import threading

class Client:
    def __init__(self, ip: str, port: int, username: str):
        self.ip = ip
        self.port = port
        self.username = username.encode('utf-8')
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.ip, self.port))


    def write(self):
        while True:
            try:
                msg = f"{self.username}: {input(' ')}"
                self.clientSocket.send(msg.encode('utf-8'))
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"And error occured {str(e)}")
                break

    
    def read(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode('utf-8')
                print(msg)
            
            except Exception as e:
                print(f"An error occured {str(e)}")
                self.clientSocket.close()
                break

    def start(self):
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
        print("Keyboard interupted!!!")
        sys.exit()

