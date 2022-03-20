# SETTINGS FILE
import os

HEADER = 1024
HOST = 'localhost'
PORT = 5050
ADDR = (HOST, PORT)

FORMAT = 'utf-8'

SHUT_DOWN_SERVER = False

CONNECTED_CLIENTS = {}

ROUTE_MAP = {}

CHAR_MAP = {}

STATIC_PATH = os.path.abspath(os.getcwd()).replace('\\','/') + '/root/client/static'
