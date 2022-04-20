import threading
import asyncio
import websockets
import time

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
    
    async def handler(self, websocket):
        self.logger.info('New Connection...')
        self.connected.add(websocket)
        
        await websocket.send('Hello User!')
        
        async for message in websocket:
            print(message)

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
