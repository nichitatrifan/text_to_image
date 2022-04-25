
import threading
import asyncio

from root.server.request_handler import ThreadedTCPRequestHandler
from root.server.thread_server import *
from root.side_modules.settings import *
            
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
                server_thread.join(0.8) # waits until the thread terminates
                ws_server.ws_thread.join(0.1)
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
