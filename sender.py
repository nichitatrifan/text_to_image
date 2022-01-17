'''Sender Class'''

import json
import socket

from number import generate_prime_number, generate_random_number, N_SIZE

class Sender:
    def __init__(self, host_port):
        # AF_INET refers to the address-family ipv4
        # SOCK_STREAM means connection-oriented TCP protocol

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect(host_port)
        self.pixels = []

    def key_exchange(self, key):
        for _l in key:
            print(f'LETTER: {_l}')
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

            self._s.sendall(f'{json.dumps(data)}\n'.encode())
            jsn = self._s.recv(1024).decode() # decodes 1024 bytes

            fro = json.loads(jsn)

            A_prime = []
            for B,aa,h in zip(fro['B'],a,data['h']):
                A_prime.append(pow(B,aa,h) % 200)
            self.pixels.append(tuple(A_prime))

            if A_prime:
                print(f'Added RGB value: {A_prime}')

    def close(self):
        self._s.close()
