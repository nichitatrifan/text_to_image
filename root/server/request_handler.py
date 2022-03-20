import socketserver
import socket
import sys
import traceback

import root.side_modules.settings as st

from root.server.logger import Logger
from root.server.http_parser import HTTPParser
from root.server.views import *

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
                raw_data = client_socket.recv(1024).decode(st.FORMAT)
                if raw_data:

                    parsed_request = HTTPParser.parse_http_request(raw_data)

                    if 'Referer' in parsed_request['headers']:
                        child_request = True

                    if parsed_request:
                        if parsed_request['end_point'] in st.ROUTE_MAP: 
                            response_data = st.ROUTE_MAP[parsed_request['end_point']](
                                parsed_request
                                )
                            client_socket.sendall(response_data.encode(st.FORMAT))
                        else:
                            #TODO handling other requests 
                            pass

            except socket.timeout as te:
                pass

            except Exception as ex:
                #TODO the exception is too general! Change Later!
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

    def exchange_messages(self, data, char_map):
        ''' Exchanges the messages between server and the client '''
        i = 0
        self.logger.info('char map: ')
        self.logger.info(char_map)
        message = ''
        while i < len(data) - 2:
            for key in st.CHAR_MAP:
                if st.CHAR_MAP[key] == [data[i], data[i+1], data[i+2]]:
                    message += key
            i += 3
        self.logger.info('Message: ' + message)

if __name__ == '__main__':
    pass