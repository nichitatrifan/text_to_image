from ntpath import join
import os
from pydoc import tempfilepager
import socketserver
import json
import socket
import string
import random
import sys
import ast
import traceback

import root.side_modules.settings as st

from datetime import datetime

from root.side_modules.number import generate_prime_number, N_SIZE
from root.side_modules.settings import *
from root.side_modules.logger import Logger

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler, Logger):
    def __init__(self, request, client_address, server) -> None:
        self.char_map = {}
        Logger.__init__(self)
        super().__init__(request, client_address, server)
    
    def init_char_map(self, seed):
        printable_string = string.printable
        printable_list = []
        for char in printable_string:
            printable_list.append(char)
        random.Random(seed).shuffle(printable_list)
        for char in printable_list:
            self.char_map[char] = None
    
    def add_to_client_pool(self, client_ip, client_port):
        addresses = st.CONNECTED_CLIENTS.keys()
        if client_ip not in addresses:
            temp = [client_port]
            st.CONNECTED_CLIENTS[client_ip] = temp
        else:
            st.CONNECTED_CLIENTS[client_ip].append(client_port)
        self.logger.info('CLIENTS: ' + str(st.CONNECTED_CLIENTS))
    
    def remove_client_from_pool(self, client_ip, client_port):
        addresses = st.CONNECTED_CLIENTS.keys()
        if client_ip in addresses:
            st.CONNECTED_CLIENTS[client_ip].remove(client_port)
        self.logger.info('CLIENTS: ' + str(st.CONNECTED_CLIENTS))
    
    def parse_http_request(self, raw_data):
        """ Parses HTTP request """
        if not raw_data:
            return None

        method_path, headers_body = raw_data.split('\r\n',1)
        method_path = method_path.replace('%22','')
        headers, body = headers_body.split('\r\n\r\n', 1)
        
        end_point = method_path.split(' ')[1]
        if end_point[-1] == '/':
            end_point_list  = list(end_point)
            end_point_list[-1] = ''
            end_point = ''.join(end_point_list)
        
        text = headers.split('\r\n')
        if body:
            body = body.replace('\r\n', '')
            self.logger.info(body)
            body = ast.literal_eval(body)
        else:
            body = {}

        # self.logger.info('request path: ' + str(method_path))
        self.logger.info('end_point: ' + str(end_point))
        # self.logger.info('headers:\n'+headers)

        head_dict = {}
        for element in text:
            key, value = element.split(':',1) #TODO replace the initial space
            head_dict[key] = value

        # self.logger.info('headers:\n'+str(head_list))
        
        return_data = {
            'end_point': str(end_point),
            'headers': head_dict,
            'body': body
        }

        # self.logger.info(return_data)
        return return_data
    
    def parse_http_response(self, data:dict, status_code:str) -> str:
        date_obj = datetime.now()
        date = str(date_obj.day) + '_' + str(date_obj.month)  + \
            '_' + str(date_obj.year) + '_' + str(date_obj.hour) + '_' + str(date_obj.minute) +\
            '_' + str(date_obj.second)
        
        content_len = len(json.dumps(data).encode('utf-8'))

        response = f'HTTP/1.1 {status_code}\r\n' +\
            f'Date: {date}\r\n' +\
            'Server: localhost\r\n' +\
            f'Content-Length: {content_len}\r\n' +\
            'Connection: Closed\r\n' +\
            'Content-Type: text/html\r\n'+\
            '\r\n'
        
        response += str(json.dumps(data)) + '\r\n'
        return response
    
    def handle(self):
        client_socket = self.request
        addr = self.client_address
        client_ip, client_port = addr
        self.add_to_client_pool(client_ip, client_port)

        self.logger.info(f'{addr} connected.')

        client_socket.settimeout(0.5)
        connected = True
        child_request = False
        while connected and not st.SHUT_DOWN_SERVER and not child_request:
            try:
                raw_data = client_socket.recv(1024).decode(st.FORMAT)
                if raw_data:

                    parsed_request = self.parse_http_request(raw_data)

                    if 'Referer' in parsed_request['headers']:
                        # self.logger.info('Refer header: ' + parsed_request['headers']['Referer'])
                        child_request = True

                    #TODO change endpoints formating
                    if parsed_request['end_point'] == '/key_exchange':
                        self.handle_key_exchange(parsed_request['body'])

                    elif parsed_request['end_point'] == '/seed_exchange':
                        self.handle_seed_exchange(parsed_request['body'])

                    elif parsed_request['end_point'] == '/message':
                        self.exchange_messages(parsed_request['body'], self.char_map)

                    elif parsed_request['end_point'] == '/index':
                        self.index()
                    else:
                        self.logger.info('Does nothing now')
                        pass #TODO search the url or internal path for static files

            except socket.timeout as te:
                pass

            except Exception as ex:        #TODO the exception is too general! Change Later!
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                self.logger.warning(str(ex))
                traceback.print_tb(exception_traceback)
                connected = False
                self.logger.info('[THREAD] Function Ended Execution Through Exception!')
        
        if child_request:
            self.remove_client_from_pool(client_ip, client_port)
        
        self.logger.info('[THREAD] Function Ended Execution')
        return 1

    def index(self):
        client_socket = self.request
        resource_path = os.path.abspath(os.getcwd()).replace('\\','/') + '/root/client/static/index.html'

        with open(resource_path, 'r') as fl:
            htm_text = fl.read()
        
        # self.logger.info(htm_text)

        status_code = '200 OK'
        response_data = self.parse_http_response(htm_text, status_code)
        client_socket.sendall(response_data.encode(st.FORMAT))

    def handle_seed_exchange(self, data):
        """ Handles the seed exchange between the client and the server """
        client_socket = self.request
        addr = self.client_address

        A, n, h = data['A'], data['n'], data['h']
        
        seed_b_private = generate_prime_number(N_SIZE)
        seed_B_public = pow(n, seed_b_private, h)
        seed_num = pow(A, seed_b_private, h)
        self.logger.info(' seed number: ' + str(seed_num))
        return_data = {
            'B': seed_B_public
        }
        self.init_char_map(seed=seed_num)
        client_socket.sendall(json.dumps(return_data).encode(st.FORMAT))

    def handle_key_exchange(self, data):
        ''' Exchanges the keyes between server and the client '''
        client_socket = self.request
        addr = self.client_address

        n_data = data['n']
        h_data = data['h']
        A_data = data['A']
        self.logger.info(f'A list: {A_data}')
        self.logger.info(f'h list: {h_data}')
        self.logger.info(f'n list: {n_data}')

        if data:
            b = []
            B_public = []
            B_private = []

            for n_list, h_list, A_list in zip(n_data, h_data, A_data): # unpack to single list
                temp_b = []
                temp_B_public = []
                temp_B_private = []
                for n, h, A in zip(n_list, h_list, A_list): # unpack to individual values
                    bb = generate_prime_number(N_SIZE)
                    temp_b.append(bb)
                    temp_B_public.append(pow(n,bb,h))
                B_public.append(temp_B_public)
                b.append(temp_b)
                
                # Generating private Key
                for A, bb, h in zip(A_list, temp_b, h_list):
                    temp_B_private.append(str(pow(A, bb, h) % 200)) # B' = A^b (mod h)
                B_private.append(temp_B_private)

            if B_private:
                for  B in B_private:
                    for key in self.char_map:
                        if not self.char_map[key]:
                            self.char_map[key] = B_private
                            break
                self.logger.info(f'{addr} added RGB value: {B_private}')
            
            _data = { 
                'B': B_public
                }
            status_code = '200 OK'
            response_data = self.parse_http_response(_data, status_code)
            client_socket.sendall(response_data.encode(st.FORMAT))
    
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
            i += 3
        self.logger.info('Message: ' + message)

if __name__ == '__main__':
    pass