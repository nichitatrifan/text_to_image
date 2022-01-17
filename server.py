from email.errors import NonPrintableDefect
import socket
import threading
import json

from number import generate_prime_number, generate_random_number, N_SIZE


HEADER = 1024
PORT = 5050
HOST = 'localhost'
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    
    while connected:
        try:
            data = json.loads(conn.recv(1024).strip().decode(FORMAT))
        except:
            print('[NO DATA HAS BEEN SENT]')
            connected = False
            data = None

        if data:
            # msg_length = int(msg_length)
            # msg = conn.recv(msg_length).decode(FORMAT)
            # if msg == DISCONNECT_MESSAGE:
            #     connected = False
            # print(f'[{addr}] {msg}')
            print(data)
            b = []
            B = []
            pixels = []

            for n,h in zip(data['n'], data['h']):
                bb = generate_prime_number(N_SIZE)
                b.append(bb)
                B.append(pow(n,bb,h))

            return_data = { 'B': B }
            conn.sendall(f'{json.dumps(return_data)}\n'.encode(FORMAT)) # encodes to a byte array
            
            B_prime = []
            for A,bb,h in zip(data['A'], b, data['h']):
                B_prime.append(pow(A,bb,h) % 200)
            pixels.append(tuple(B_prime))

            if B_prime:
                print(f'{addr} added RGB value: {B_prime}')

    conn.close()

def start():
    server.listen()
    print(f'[LISTENNING] Server is listenning on {HOST} {PORT}')
    while True:
        try:
            client_socket, addr = server.accept() # it waits here for a new connection
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
            print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
        except KeyboardInterrupt as kyi:
            print('[KeyBoard Interrupt]')
            server.close()

if __name__ == '__main__':
    print('Starting the server at: ' + str(HOST) + ' ' + str(PORT))
    start()