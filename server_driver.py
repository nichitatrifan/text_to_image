
import threading
import asyncio
import websockets
import json
import numpy as np

from base64 import b64decode
from PIL import Image
from root.server.request_handler import ThreadedTCPRequestHandler
from root.server.logger import Logger
from root.server.thread_server import *
from root.side_modules.settings import *

class WebSocketThread(Logger):
    def __init__(self) -> None:
        Logger.__init__(self,'WebSocket')
        self.tasks_pending = None
        self.loop = None
        self.ws_thread = None
        self.ws_object = None
        self.connected = set()

    def start_loop(self, loop:asyncio.BaseEventLoop, server):
        """ Starting an event loop in a separate thread """
        self.loop = loop
        self.ws_event = loop.run_until_complete(server)
        loop.run_forever()
        
    def start_ws(self) ->threading.Thread:
        new_loop = asyncio.new_event_loop()
        self.ws_object = websockets.serve(self.handler, HOST, WS_PORT, loop=new_loop)
        self.ws_thread = threading.Thread(target=self.start_loop, args=(new_loop, self.ws_object))
        self.ws_thread.start()
        print('WS is listening on 127.0.0.1:5051')
    
    def decode_message(self, data_uri:str, count:int):
        DECODE_MAP = {'51148117': '0', '74167175': '1', '9555114': '2', '12648163': '3', '9421690': '4', '80124163': '5', '656086': '6', '1322684': '7', '488774': '8', '17345172': '9', '8010687': 'a', '17520446': 'b', '8610979': 'c', '2915971': 'd', '77111111': 'e', '18188150': 'f', '1054359': 'g', '17016937': 'h', '147198': 'i', '97882': 'j', '170213182': 'k', '190221125': 'l', '343259': 'm', '2296144': 'n', '13931': 'o', '142174125': 'p', '4922342': 
            'q', '6817850': 'r', '172190109': 's', '151101111': 't', '138642': 'u', '24107144': 'v', '135133120': 'w', '3018032': 'x', '14445102': 'y', '5713937': 'z', '1956953': 'A', '18059': 'B', '4695106': 'C', '111112196': 'D', '1507291': 'E', '2416497': 'F', '2068149': 'G', '22100106': 'H', '13650205': 'I', '24149109': 'J', '6618476': 'K', '15277181': 'L', '836381': 'M', '1279552': 'N', '5513384': 'O', '11947102': 'P', '417944': 'Q', '87108122': 'R', '6228184': 'S', '83212121': 'T', '35120180': 'U', '5713789': 'V', '18162166': 'W', '4522599': 'X', '14419254': 'Y', '111107208': 'Z', '14856177': '!', '3934166': '"', '423865': '#', '4219587': '$', '12721375': '%', '64145': '&', '182185149': "'", '14212472': '(', '1096082': ')', '1860176': '*', '803257': '+', '754769': ',', '16150187': '-', '55134100': '.', '1014761': '/', '82228130': ':', '158127180': ';', '324264': '<', '1366534': '=', '142215130': '>', '1573526': '?', '16464159': '@', '134100219': '[', '5916026': '\\', '10419882': ']', '6546178': '^', '12549214': '_', '8232128': '`', '8317087': '{', '7613538': '|', '12953140': '}', '1718069': '~', '51163173': ' ', '15172116': '\t', '146178102': '\n', '2197210': '\r', '17112170': '\x0b', '3110576': '\x0c'}
        header, encoded_text = data_uri.split(',', 1)
        
        image_data = b64decode(encoded_text)
        with open(f'char_maps/image_{count}.png', 'wb') as png_file:
            png_file.write(image_data)
        
        message_image = Image.open(f'char_maps/image_{count}.png')
        width, height = message_image.size
        pixel_values = list(message_image.getdata())
        if message_image.mode == 'RGBA':
            channels = 4
        pixel_values = np.array(pixel_values).reshape((width, height, channels))
        # print(pixel_values)
        message_values = []
        for i in range(int(width/10)):
            message_values.append([pixel_values[i,0][0], pixel_values[i,0][1], pixel_values[i,0][2]])
            # print(pixel_values[i,0])
        print(message_values)
        message_str = ''
        for i in range(len(message_values)):
            key = str(message_values[i][0]) + str(message_values[i][1]) + str(message_values[i][2])
            message_str += DECODE_MAP[key]
        return message_str

    async def handler(self, websocket):
        self.logger.info('New Connection...')
        self.connected.add(websocket)
        
        await websocket.send('Hello User!')
        async for message in websocket:
            message_dict = json.loads(message)
            data_uri = message_dict['text']
            message_text = self.decode_message(data_uri, message_dict['count'])
            print('Actual Message :' + message_text)
            # echoing the message
            message_dict['count'] = 1 + int(message_dict['count'])
            await websocket.send(json.dumps(message_dict))
            
if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.logger.info(f'LISTENNING {HOST} {PORT}')

    with server:
        # Start a thread with the server -- that thread will then start other threads
        # one thread for one client connection
        try:
            server_thread = threading.Thread(target=server.serve_forever, args=(0.5,))
            server_thread.daemon = True
            server_thread.start()
            
            ws_server = WebSocketThread()
            ws_server.start_ws()

            while server_thread.is_alive():
                server_thread.join(1.0) # waits until the thread terminates
                #ws_thread.join(0.5)
                server.logger.info(f'ACTIVE CONNECTIONS {threading.active_count() - 4}')

        except KeyboardInterrupt as kyi:
            server.logger.warning('KeyBoard Interrupt')
            # ws_server.loop.close()

            server.signal_shut_down()
            server.shutdown()
        finally:
            # CancelledError
            for task in asyncio.all_tasks(ws_server.loop):
                #print(task, end='\n\n')
                task.cancel()
            ws_server.loop.stop()
            ws_server.ws_thread.join()
