'''Sender Class'''

import json
import socket
import string
import os

from ..side_modules.number import generate_prime_number, N_SIZE
from ..side_modules.settings import *
from datetime import datetime

class Sender:
    def __init__(self, host_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(host_port)

        self.pixels = []
        self.printables_string = string.printable
        self.char_map = {}
        date_obj = datetime.now()
        self.date = str(date_obj.day) + '_' + str(date_obj.month)  + \
            '_' + str(date_obj.year) + '_' + str(date_obj.hour) + '_' + str(date_obj.minute) +\
            '_' + str(date_obj.second)  
        self.json_path = os.path.abspath(os.getcwd()).replace('\\','/') + f'/char_maps/char_map_{self.date}.json'  

    def init_char_map(self):
        for char in self.printables_string:
            self.char_map[char] = []

    def key_exchange(self):
        header = 'key_exchange'

        self.init_char_map()
        for char in self.char_map:
            print(f'CHAR: {char}')

            a = []
            data = {
                'n': [],
                'h': [],
                'A': []
            }
            for i in range(3):
                n  = generate_prime_number(N_SIZE)
                aa = generate_prime_number(N_SIZE)
                h  = generate_prime_number(N_SIZE)

                a.append(aa)                  # secret number
                data['n'].append(n)           # generator number
                data['h'].append(h)           # mod number
                data['A'].append(pow(n,aa,h)) # public key A = (n)^aa (mod h) 

            self.client.sendall(json.dumps({'header':header, 'data':data}).encode())

            jsn = self.client.recv(1024).decode()
            fro = json.loads(jsn)

            A_prime = []
            for B,aa,h in zip(fro['B'], a, data['h']):
                A_prime.append(pow(B,aa,h) % 200) # A' = B^aa (mod h)
            self.pixels.append(tuple(A_prime))

            if A_prime:
                print(f'Added RGB value: {A_prime}')
                self.char_map[char] = A_prime
        
    def save_char_map(self):
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.char_map, file, indent=4, ensure_ascii=False)
    
    def send_message(self, message:str)->None:
        '''Sends the encoded message in the body'''
        
        encoded_message = []
        header = 'message'

        for chr in message:
            r, g, b = self.char_map[chr]
            encoded_message += [str(r), str(g), str(b)]
        print(encoded_message)

        self.client.sendall(json.dumps({'header':header,
            'data':encoded_message}).encode())

    def close(self):
        self.client.close()
