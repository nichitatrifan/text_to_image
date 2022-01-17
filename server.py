import socket
import threading
import json
import logging

from number import generate_prime_number, generate_random_number, N_SIZE
from settings import *


class ThreadServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        logging.basicConfig()
        self.logger = logging.getLogger('TCPLogger')
        self.logger.setLevel(logging.INFO)

    def handle_client(self, client_socket, addr):
        self.logger.info(f'[NEW CONNECTION] {addr} connected.')
        connected = True
        
        while connected:
            try:
                data = json.loads(client_socket.recv(1024).strip().decode(FORMAT))
            except:
                self.logger.warning('[NO DATA HAS BEEN SENT]')
                connected = False
                data = None

            if data:
                # msg_length = int(msg_length)
                # msg = conn.recv(msg_length).decode(FORMAT)
                # if msg == DISCONNECT_MESSAGE:
                #     connected = False
                # print(f'[{addr}] {msg}')
                
                # print(data)
                
                b = []
                B = []
                pixels = []

                for n,h in zip(data['n'], data['h']):
                    bb = generate_prime_number(N_SIZE)
                    b.append(bb)
                    B.append(pow(n,bb,h))

                return_data = { 
                    'B': B
                    }

                client_socket.sendall(f'{json.dumps(return_data)}\n'.encode(FORMAT)) # encodes to a byte array
                
                B_prime = []
                for A,bb,h in zip(data['A'], b, data['h']):
                    B_prime.append(pow(A,bb,h) % 200)
                pixels.append(tuple(B_prime))

                if B_prime:
                    self.logger.info(f'{addr} added RGB value: {B_prime}')

        client_socket.close()

    def start(self):
        self.server.listen()
        self.logger.info(f'[LISTENNING] {HOST} {PORT}')

        while True:
            try:
                client_socket, addr = self.server.accept() # it waits here for a new connection
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
                self.logger.info(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
            except KeyboardInterrupt as kyi:
                self.logger.warning('[KeyBoard Interrupt]')
                self.server.close()


if __name__ == '__main__':
    print('Starting the server at: ' + str(HOST) + ' ' + str(PORT))
    my_server = ThreadServer()
    my_server.start()