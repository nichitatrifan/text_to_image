'''Receiver Class'''

import json
import socketserver

from side_modules.number import generate_prime_number, generate_random_number, N_SIZE

class Receiver(socketserver.StreamRequestHandler):
    def __init__(self, *args):
        self.pixels = []
        super().__init__(*args)

    def handle(self):
        while True:
            self.data = json.loads(self.rfile.readline(1024).strip().decode())
            #self.data = json.loads(self.request.recv(1024).strip().decode())
            
            if self.data:
                print(f'{self.client_address[0]} sent: {self.data}')

            b = []
            B = []
            for n,h in zip(self.data['n'],self.data['h']):
                bb = generate_prime_number(N_SIZE)
                b.append(bb)
                B.append(pow(n,bb,h))

            return_data = { 'B': B }
            self.wfile.write(f'{json.dumps(return_data)}\n'.encode()) # encodes to a byte array
            #self.request.sendall(f'{json.dumps(return_data)}\n'.encode())
            
            B_prime = []
            for A,bb,h in zip(self.data['A'],b,self.data['h']):
                B_prime.append(pow(A,bb,h) % 200)
            self.pixels.append(tuple(B_prime))

            if B_prime:
                print(f'{self.client_address[0]} added RGB value: {B_prime}')

def main():
    HOST, PORT = 'localhost', 9999

    with socketserver.TCPServer((HOST,PORT), Receiver) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt as kbi:
            print()
            server.shutdown()

if __name__ == '__main__':
    main()
