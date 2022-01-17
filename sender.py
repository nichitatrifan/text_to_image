'''Sender Class'''

import json
import socket
import string
from time import sleep

from number import generate_prime_number, generate_random_number, N_SIZE
from settings import *


class Sender:
    def __init__(self, host_port):
        # AF_INET refers to the address-family IPv4
        # SOCK_STREAM means connection-oriented TCP protocol

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(host_port)
        self.pixels = []
        self.printables_string = string.printable
        self.char_map = {}

    def init_char_map(self):
        for char in self.printables_string:
            self.char_map[char] = []

    def key_exchange(self):
        self.init_char_map()
        for char in self.char_map:
            print(f'CHAR: {char}')

            a = []
            data = {
                'n': [],
                'h': [],
                'A': []
            }
            for _i in range(3):
                n  = generate_prime_number(N_SIZE)
                aa = generate_prime_number(N_SIZE)
                h  = generate_prime_number(N_SIZE)

                data['n'].append(n)
                a.append(aa)
                data['h'].append(h)
                data['A'].append(pow(n,aa,h))

            self.client.sendall(f'{json.dumps(data)}\n'.encode())
            jsn = self.client.recv(1024).decode() # decodes 1024 bytes

            fro = json.loads(jsn)

            A_prime = []
            for B,aa,h in zip(fro['B'],a,data['h']):
                A_prime.append(pow(B,aa,h) % 200)
            self.pixels.append(tuple(A_prime))

            if A_prime:
                print(f'Added RGB value: {A_prime}')
                self.char_map[char] = A_prime

    def close(self):
        self.client.close()
