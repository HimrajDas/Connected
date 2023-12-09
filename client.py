import socket
import errno
import sys
import logging

HEADER_LENGTH = 10
logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
class Client:
    
    def __init__(self, ip: str, port: int, username: str):
        self.ip = ip
        self.port = port
        self.username = username.encode('utf-8')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)
        

    
    def connect(self):
        try:
            self.client_socket.connect((self.ip, self.port))
            self.send_username()
        except Exception as e:
            print(f"Error connecting to the server: {str(e)}")
            sys.exit()


    def send_username(self):
        username_header = f"{len(self.username):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + self.username)


    def send_msg(self, msg):
        try:
            msg = msg.encode('utf-8')
            msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(msg_header + msg)
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            sys.exit()


    def recv_msg(self):
        try:
            while True:
                username_header = self.client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection closed by the server!")
                    sys.exit()
                
                username_length = int(username_header.decode('utf-8').strip())
                username = self.client_socket.recv(username_length).decode('utf-8')

                msg_header = self.client_socket.recv(HEADER_LENGTH)
                msg_length = int(msg_header.decode('utf-8').strip())
                msg = self.client_socket.recv(msg_length.decode('utf-8'))

                print(f"{username} > {msg}")
        
        except (IOError, ConnectionResetError, TimeoutError) as e:
            print(f"Reading error: {str(e)}")
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print(f"Reading error: {str(e)}")
                sys.exit()
            

        except Exception as e:
            print(f"Reading error: {str(e)}")
            sys.exit()


if __name__ == "__main__":
    try:
        username = input("Username: ")
        chat_client = Client("127.0.0.1", 12000, username)

        while True:
            message = input(f"{username} > ")
            if message:
                chat_client.send_msg(message)
            
            chat_client.recv_msg()
    except KeyboardInterrupt:
        print("Keyboard interupted!!")
        sys.exit()