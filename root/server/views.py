import os
import string
import random
import root.side_modules.settings as st

from root.server.router import Router
from root.server.http_parser import HTTPParser
from root.side_modules.number import *

# a = [37199, 56843, 48523]

@Router('/index')
def index(parsed_request:dict) -> str:
    """ Uploads the starting page """
    resource_path = os.path.abspath(os.getcwd()).replace('\\','/') + '/root/client/static/index.html'

    with open(resource_path, 'r') as fl:
        html_text = fl.read()

    status_code = '200 OK'

    return HTTPParser.parse_http_response(html_text, status_code)

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
                for key in st.CHAR_MAP:
                    if not st.CHAR_MAP[key]:
                        st.CHAR_MAP[key] = B_private
                        break
        
        _data = { 
            'B': B_public
            }
        status_code = '200 OK'

        return HTTPParser.parse_http_response(_data, status_code)
    else:
        _data = { 
            'B': 'None'
            }
        status_code = '400 Bad Request'

        return HTTPParser.parse_http_response(_data, status_code)

@Router('/seed_exchange')
def handle_seed_exchange(parsed_request:dict):
    """ Handles the seed exchange between the client and the server """

    A, n, h =  parsed_request['body']['A'],  parsed_request['body']['n'],  parsed_request['body']['h']

    seed_b_private = generate_prime_number(N_SIZE)
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

    return HTTPParser.parse_http_response(_data, status_code)
