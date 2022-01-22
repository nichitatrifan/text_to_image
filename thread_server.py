import threading
import socketserver
import json
import logging

from number import generate_prime_number, generate_random_number, N_SIZE
from settings import *


class Logger:
    def __init__(self) -> None:    
        logging.basicConfig()
        self.logger = logging.getLogger('TCPLogger')
        self.logger.setLevel(logging.INFO)


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler, Logger):
    def __init__(self, request, client_address, server) -> None:
        Logger.__init__(self)
        super().__init__(request, client_address, server)
    
    def handle(self):
        connected = True
        client_socket = self.request
        addr = self.client_address

        self.logger.info(f'[NEW CONNECTION] {addr} connected.')

        while connected:
            try:
                data = json.loads(client_socket.recv(1024).strip().decode(FORMAT))
            except:
                self.logger.warning('[NO DATA HAS BEEN SENT]')
                connected = False
                data = None

            if data:
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

        self.logger.info('[THREAD] Function Ended Execution')
        return 1


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, Logger):
    # need to create a function for the active connections displaying
    # use that function as a separate thread
    def __init__(self, *args) -> None:
        Logger.__init__(self)
        super().__init__(*args)


if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.logger.info(f'[LISTENNING] {HOST} {PORT}')

    with server:    
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        try:
            server_thread = threading.Thread(target=server.serve_forever, args=(0.5,))
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True # must be set before start()
            server_thread.start()

            while server_thread.is_alive():
                server_thread.join(1.0) # waits until the thread terminates
                server.logger.info(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

            # print("Server loop running in thread:", server_thread.name)
        except KeyboardInterrupt as kyi:
            server.logger.warning('[KeyBoard Interrupt]')
            server.shutdown()