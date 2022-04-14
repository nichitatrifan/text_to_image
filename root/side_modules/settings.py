# SETTINGS FILE
import os

PAKCET_SIZE = 8192
HOST = 'localhost'
PORT = 5050
WS_PORT = 5051
ADDR = (HOST, PORT)

FORMAT = 'utf-8'

SHUT_DOWN_SERVER = False

CONNECTED_CLIENTS = {}
ROUTE_MAP = {}
CHAR_MAP = {}

STATIC_PATH = os.path.abspath(os.getcwd()).replace('\\','/') + '/root/client/static'

EXTENSION_TYPES_REGEX = r'.(jpg|json|htm|html|ico|js|jpg|css)$'
EXTENSION_TYPES = {
    '.ico': 'image/vnd.microsoft.icon',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.json': 'application/json',
    '.css': 'text/css'
}
