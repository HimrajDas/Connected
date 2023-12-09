import socket
import select
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.HEADER_LENGTH = 10

        # create the socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]
        self.clients = {}


    def run_server(self):
        print(f"[LISTENING] for connection on {self.ip}:{self.port}")
        try:
            while True:
                read_sockets, _, exception_socket = select.select(
                    self.sockets_list, [], self.sockets_list
                )

                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        self.handle_new_connection()
                    else:
                        self.handle_client_msg(notified_socket)

                for notified_socket in exception_socket:
                    self.remove_socket(notified_socket)
        except KeyboardInterrupt:
            print("Keyboard Interuption occured!!")
            self.cleanup()
            sys.exit()


    def handle_new_connection(self):
        client_socket, client_adress = self.server_socket.accept()
        user = self.rcv_msg(client_socket)

        if user is not False:
            self.sockets_list.append(client_socket)
            self.clients[client_socket] = user
            print(
                f"Accepted new connection from {client_adress[0]}:{client_adress[1]}",
                f"username:{user['data'].decode('utf-8')}",
            )


    def rcv_msg(self, client_socket):
        try:
            msg_header = client_socket.recv(self.HEADER_LENGTH)

            if not len(msg_header):
                return False

            msg_length = int(msg_header.decode("utf-8").strip())

            return {"header": msg_header, "data": client_socket.recv(msg_length)}

        except:
            return False

    def handle_client_msg(self, notified_socket):
        msg = self.rcv_msg(notified_socket)

        if msg is False:
            print(f"Closed connection from {self.clients[notified_socket]['data']}")
        if msg:
            user = self.clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')
            self.broadcast_msg(notified_socket, user, msg)


    def remove_socket(self, notified_socket):
        self.sockets_list.remove(notified_socket)
        del self.clients[notified_socket]


    def broadcast_msg(self, sender_socket, sender_user, msg):
        for client_socket in self.clients:
            if client_socket != sender_socket and client_socket in self.sockets_list:
                try:
                    client_socket.send(
                        sender_user["header"]
                        + sender_user["data"]
                        + msg["header"]
                        + msg["data"]
                    )
                except:
                    logger.warning(f"Client disconnected during message broadcasting: {client_socket}")
                    self.remove_socket(client_socket)


    def cleanup(self):
        self.server_socket.close()


if __name__ == "__main__":
    
    server = Server("127.0.0.1", 12000)
    server.run_server()
    
