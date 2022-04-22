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
            for i, key in enumerate(st.CHAR_MAP):
                print(key, B_private[i])
                st.CHAR_MAP[key] = B_private[i]
                # for key in st.CHAR_MAP:
                #     if not st.CHAR_MAP[key]:
                #         st.CHAR_MAP[key] = B_private
                #         break
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

@Router('/cop_exchange')
def handle_cop_exchange(parsed_request:dict):
    """ Handles the cop exchange between the client and server """

    # check what info is in the dict
    if parsed_request['body']:
        n_data = parsed_request['body']['n']
        h_data = parsed_request['body']['h']
        A_data = parsed_request['body']['A']

        b = []
        B_public = []
        B_private = []

        for n, h, A in zip(n_data, h_data, A_data): # unpack to individual values
            bb = random.randint(1, h - 1)
            b.append(bb)
            B_public.append(pow(n,bb,h))
            B_private.append(str(pow(A, bb, h) % 55)) # B' = A^b (mod h)

        # add cop values to char map
        if B_private:
            for key in st.CHAR_MAP:
                st.CHAR_MAP[key][0] = int(st.CHAR_MAP[key][0]) + int(B_private[0])
                st.CHAR_MAP[key][1] = int(st.CHAR_MAP[key][1]) +  int(B_private[1])
                st.CHAR_MAP[key][2] = int(st.CHAR_MAP[key][2]) +  int(B_private[2])
                # st.CHAR_MAP[key] = [sum(B) for B in zip(st.CHAR_MAP[key], B_private)] # summation of an array with a value!!!!
        print(st.CHAR_MAP)
        for key in st.CHAR_MAP:
            value = str(st.CHAR_MAP[key][0]) + str(st.CHAR_MAP[key][1]) + str(st.CHAR_MAP[key][2])
            st.DECODE_MAP[value] = key
        print(st.DECODE_MAP)
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

@Router('/open_chat')
def open_chat(parsed_request:dict):
    resource_path = st.STATIC_PATH + '/websockets_index.html'

    with open(resource_path, 'rb') as fl:
        html_text = fl.read()

    status_code = '200 OK'
    response = {
        'header': HTTPParser.parse_http_response_header(html_text, 
                status_code, 'text/html').encode(st.FORMAT),
        'payload': html_text
    }
    return response
