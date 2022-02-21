import json
import ast

from datetime import datetime

class HTTPParser:
    def __init__(self) -> None:
        pass

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
            body = ast.literal_eval(body)
        else:
            body = {}

        head_dict = {}
        for element in text:
            key, value = element.split(':',1) #TODO replace the initial space
            head_dict[key] = value
        
        return_data = {
            'end_point': str(end_point),
            'headers': head_dict,
            'body': body
        }

        return return_data
    