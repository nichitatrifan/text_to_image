import socketserver
import socket
import sys
import traceback
import re
import asyncio

import root.side_modules.settings as st

from root.server.logger import Logger
from root.server.http_parser import HTTPParser
from root.server.views import *
from root.websockets.app import main as ws_main

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler, Logger):
    def __init__(self, request, client_address, server) -> None:
        Logger.__init__(self)
        super().__init__(request, client_address, server)

    def add_to_client_pool(self, client_ip, client_port):
        addresses = st.CONNECTED_CLIENTS.keys()
        if client_ip not in addresses:
            temp = [client_port]
            st.CONNECTED_CLIENTS[client_ip] = temp
        else:
            st.CONNECTED_CLIENTS[client_ip].append(client_port)
        self.logger.info('CLIENTS: ' + str(st.CONNECTED_CLIENTS))

    def remove_from_client_pool(self, client_ip, client_port):
        addresses = st.CONNECTED_CLIENTS.keys()
        if client_ip in addresses:
            st.CONNECTED_CLIENTS[client_ip].remove(client_port)
        self.logger.info('CLIENTS: ' + str(st.CONNECTED_CLIENTS))

    def handle(self):
        client_socket = self.request
        client_socket.settimeout(0.5)

        addr = self.client_address
        client_ip, client_port = addr

        self.logger.info(f'{addr} connected.')
        self.add_to_client_pool(client_ip, client_port)

        connected = True
        child_request = False

        while connected and not st.SHUT_DOWN_SERVER and not child_request:
            try:
                raw_data = client_socket.recv(st.PAKCET_SIZE).decode(st.FORMAT)
                if raw_data:

                    parsed_request = HTTPParser.parse_http_request(raw_data)

                    if parsed_request:
                        self.logger.info(parsed_request['method'] + ' ' + parsed_request['protocol'])
                        self.logger.info(parsed_request['headers'])
                        
                        if 'Referer' in parsed_request['headers']:
                            child_request = True
                        
                        if 'UPGRADE' in parsed_request['headers']['Connection'].upper():
                            self.websocket_handler(client_socket, parsed_request)
                        elif 'HTTP' in parsed_request['protocol'].upper():
                            self.http_handler(client_socket, parsed_request)

            except socket.timeout as te:
                pass
            
            except FileNotFoundError as er:
                self.logger.warning('RESOURCE ' + parsed_request['end_point'] + ' NOT FOUND!') 

            except Exception as ex:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno

                self.logger.warning(str(ex))
                self.logger.warning(exception_type)
                traceback.print_tb(exception_traceback)                
                self.logger.info('[THREAD] Function Ended Execution Through Exception!')
                connected = False

        if child_request:
            self.remove_from_client_pool(client_ip, client_port)
        
        self.logger.info('[THREAD] Function Ended Execution')
        return 1
    
    def get_static_resource(self, resource_path:str):
        self.logger.info(resource_path)
            
        path = st.STATIC_PATH + resource_path
        with open(path, 'rb') as st_file:
            file_payload = st_file.read()
        
        resource_extension = re.search(st.EXTENSION_TYPES_REGEX, resource_path)
        try:
            resource_type = st.EXTENSION_TYPES[resource_extension.group(0)]
        except KeyError:
            resource_type = ''

        return file_payload, resource_type
        
    def http_handler(self, client_socket:socket.socket, parsed_request:dict):
        if parsed_request['end_point'] in st.ROUTE_MAP: 
            response_dict = st.ROUTE_MAP[parsed_request['end_point']](
                parsed_request)
            
            client_socket.send(response_dict['header'])
            client_socket.send(response_dict['payload'])
            client_socket.send('\r\n'.encode(st.FORMAT))
        else:
            file_payload, resource_type = self.get_static_resource(parsed_request['end_point'])
            status_code = '200 OK'

            response_header = HTTPParser.parse_http_response_header(file_payload, 
                status_code, resource_type).encode(st.FORMAT)
            
            client_socket.send(response_header)
            client_socket.send(file_payload)
            client_socket.send('\r\n'.encode(st.FORMAT))

    async def websocket_handler(self):
        pass

if __name__ == '__main__':
    pass