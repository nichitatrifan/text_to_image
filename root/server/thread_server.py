import threading
import socketserver
import json
import logging
import string
import random

from ..side_modules.number import generate_prime_number, N_SIZE
from ..side_modules.settings import *

class Logger:
    def __init__(self) -> None:    
        logging.basicConfig()
        self.logger = logging.getLogger('[SERVER]')
        self.logger.setLevel(logging.INFO)


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler, Logger):
    def __init__(self, request, client_address, server) -> None:
        self.seed_num = 0
        self.char_map = {}
        self.init_char_map()
        Logger.__init__(self)
        super().__init__(request, client_address, server)
    
    def init_char_map(self):
        printables_string = string.printable
        for char in printables_string:
            self.char_map[char] = None
    
    def handle(self):
        client_socket = self.request
        addr = self.client_address
        self.logger.info(f'{addr} connected.')

        connected = True
        while connected:
            try:
                data = json.loads(client_socket.recv(1024).strip().decode(FORMAT))

                if data['header'] == 'key_exchange':
                    self.handle_key_exchange(data['data'])
                elif data['header'] == 'seed_exchange':
                    self.handle_seed_exchange(data['data'])
                elif data['header'] == 'message':
                    self.exchange_messages(data['data'], self.char_map)
            except:                                                         #TODO the exception is too general! Change Later!
                self.logger.warning('NO DATA HAS BEEN SENT')
                connected = False
                data = None

        self.logger.info('[THREAD] Function Ended Execution')
        return 1

    def handle_seed_exchange(self, data):
        """ Handles the seed exchange between the client and the server """
        client_socket = self.request
        addr = self.client_address

        A, n, h = data['A'], data['n'], data['h']
        
        seed_b_private = generate_prime_number(N_SIZE)
        seed_B_public = pow(n, seed_b_private, h)
        self.seed_num = pow(A, seed_b_private, h)
        self.logger.info(' seed number: ' + str(self.seed_num))
        return_data = {
            'B': seed_B_public
        }
        client_socket.sendall(json.dumps(return_data).encode(FORMAT))

    def handle_key_exchange(self, data):
        ''' Exchanges the keyes between server and the client '''
        client_socket = self.request
        addr = self.client_address
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
                B_prime.append(str(pow(A,bb,h) % 200))
            # pixels.append(B_prime)

            if B_prime:
                for key in self.char_map:
                    if not self.char_map[key]:
                        self.char_map[key] = B_prime
                        break
                self.logger.info(f'{addr} added RGB value: {B_prime}')
    
    def exchange_messages(self, data, char_map):
        ''' Exchanges the messages between server and the client '''
        i = 0
        self.logger.info('char map: ')
        self.logger.info(char_map)
        message = ''
        while i < len(data) - 2:
            for key in self.char_map:
                if self.char_map[key] == [data[i], data[i+1], data[i+2]]:
                    message += key
            # self.logger.info('char accepted: ' +\
            #     data[i] + ' ' + data[i+1] + ' ' + data[i+2])
            i += 3
        self.logger.info('Message: ' + message)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, Logger):
    # need to create a function for the active connections displaying
    # use that function as a separate thread
    def __init__(self, *args) -> None:
        Logger.__init__(self)
        super().__init__(*args)


if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.logger.info(f'LISTENNING {HOST} {PORT}')

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
                server.logger.info(f'ACTIVE CONNECTIONS: {threading.active_count() - 1}')

            # print("Server loop running in thread:", server_thread.name)
        except KeyboardInterrupt as kyi:
            server.logger.warning('KeyBoard Interrupt')
            server.shutdown()
