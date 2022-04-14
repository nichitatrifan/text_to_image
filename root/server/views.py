import json
import string
import random
import hashlib as hash
import root.side_modules.settings as st

from datetime import datetime
from root.server.router import Router
from root.server.http_parser import HTTPParser
from root.side_modules.number import *

# a = [37199, 56843, 48523]

@Router('/index')
def index(parsed_request:dict) -> str:
    """ Uploads the starting page """
    resource_path = st.STATIC_PATH + '/index.html'

    with open(resource_path, 'rb') as fl:
        html_text = fl.read()

    status_code = '200 OK'
    response = {
        'header': HTTPParser.parse_http_response_header(html_text, 
                status_code, 'text/html').encode(st.FORMAT),
        'payload': html_text
    }

    return response

@Router('/key_exchange')
def handle_key_exchange(parsed_request:dict):
    ''' Exchanges the keyes between server and the client '''

    # check what info is in the dict
    if parsed_request['body']:
        n_data = parsed_request['body']['n']
        h_data = parsed_request['body']['h']
        A_data = parsed_request['body']['A']

        b = []
        B_public = []
        B_private = []

        for n_list, h_list, A_list in zip(n_data, h_data, A_data): # unpack to single list

            temp_b = []
            temp_B_public = []
            temp_B_private = []

            for n, h, A in zip(n_list, h_list, A_list): # unpack to individual values
                bb = random.randint(1, h - 1)
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
                for key in st.CHAR_MAP:
                    if not st.CHAR_MAP[key]:
                        st.CHAR_MAP[key] = B_private
                        break
        # print('B private: \n',B_private)
        
        _data = { 
            'B': B_public
            }
        status_code = '200 OK'
        response = {
            'header': HTTPParser.parse_http_response_header(json.dumps(_data),
                    status_code, 'application/json').encode(st.FORMAT),
            'payload': json.dumps(_data).encode(st.FORMAT)
        }
        return response
    else:
        _data = { 
            'B': 'None'
            }
        status_code = '400 Bad Request'
        response = {
            'header': HTTPParser.parse_http_response_header(json.dumps(_data),
                    status_code, 'application/html').encode(st.FORMAT),
            'payload': json.dumps(_data).encode(st.FORMAT)
        }
        return response

@Router('/seed_exchange')
def handle_seed_exchange(parsed_request:dict):
    """ Handles the seed exchange between the client and the server """

    A, n, h =  parsed_request['body']['A'],  parsed_request['body']['n'],  parsed_request['body']['h']

    seed_b_private = random.randint(1, h - 1)
    seed_B_public = pow(n, seed_b_private, h)
    seed_num = pow(A, seed_b_private, h)

    printable_string = string.printable
    printable_list = []

    for char in printable_string:
        printable_list.append(char)

    random.Random(seed_num).shuffle(printable_list)
    for char in printable_list:
        st.CHAR_MAP[char] = None

    _data = { 
        'B': seed_B_public
        }
    status_code = '200 OK'
    response = {
        'header': HTTPParser.parse_http_response_header(json.dumps(_data), 
                status_code, 'application/json').encode(st.FORMAT),
        'payload': str(json.dumps(_data)).encode(st.FORMAT)
        }
    return response

# response to upgrade
# connection to websocket
#
#
# HTTP/1.1 101 Switching Protocols
# Upgrade: websocket
# Connection: Upgrade
# Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
#
#
# need to send the chat page as well
#
# compute the secret accpet header:
#   1) concatenate with '258EAFA5-E914-47DA-95CA-C5AB0DC85B11' (magic string)
#   2) perform SHA-1 (hashing algorithm)
#
#  WebSocket extensions and subprotocols are negotiated via headers during the handshake.

@Router('/upgrade-ws')
def upgrade_to_ws(parsed_request:dict):
    secret_key = parsed_request['headers']['Sec-WebSocket-Key']
    secret_key = secret_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    secret_key = hash.sha1(secret_key.encode(st.FORMAT))
    
    date_obj = datetime.now()
    date = str(date_obj.day) + '_' + str(date_obj.month)  + \
        '_' + str(date_obj.year) + '_' + str(date_obj.hour) + '_' + str(date_obj.minute) +\
        '_' + str(date_obj.second)

    response_headers = 'HTTP/1.1 101 Switching Protocols\r\n' +\
            f'Date: {date}\r\n' +\
            'Server: localhost\r\n' +\
            'Content-Length: 0\r\n' +\
            'Upgrade: websocket\r\n' +\
            'Connection: Upgrade\r\n' +\
            f'Sec-WebSocket-Accept: {secret_key}\r\n' +\
            f'Content-Type: text/html\r\n'+\
            'Access-Control-Allow-Origin: http://localhost:5050\r\n'+\
            '\r\n'
            
    response = {
        'header': response_headers.encode(st.FORMAT),
        'payload': ''
    }
    
    return response    