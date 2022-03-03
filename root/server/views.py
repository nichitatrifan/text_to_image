# DEFINE ALL THE ENDPOINTS
import os
import root.side_modules.settings as st

from root.server.router import Router
from root.server.http_parser import HTTPParser

@Router('/index')
def index(parsed_request:dict) -> str:
    resource_path = os.path.abspath(os.getcwd()).replace('\\','/') + '/root/client/static/index.html'

    with open(resource_path, 'r') as fl:
        html_text = fl.read()

    status_code = '200 OK'
    response_data = HTTPParser.parse_http_response(html_text, status_code)
    
    return response_data