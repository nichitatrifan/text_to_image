import threading
import socketserver

import root.side_modules.settings as st

from root.side_modules.settings import *
from root.side_modules.logger import Logger
from root.server.request_handler import ThreadedTCPRequestHandler


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, Logger):
    #TODO create a function for the active connections displaying
    # use that function as a separate thread
    def __init__(self, *args) -> None:
        Logger.__init__(self)
        super().__init__(*args)
    
    def signal_shut_down(self):
        st.SHUT_DOWN_SERVER = True


if __name__ == "__main__":
    server = ThreadedTCPServer((st.HOST, st.PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.logger.info(f'LISTENNING {st.HOST} {st.PORT}')

    with server:    
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        try:
            server_thread = threading.Thread(target=server.serve_forever, args=(0.5,))
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True # must be set before start()
            server_thread.start()

            while server_thread.is_alive():
                server_thread.join(1.0) # waits until the thread terminates
                server.logger.info(f'ACTIVE CONNECTIONS: {threading.active_count() - 1}')

            # print("Server loop running in thread:", server_thread.name)
        except KeyboardInterrupt as kyi:
            server.logger.warning('KeyBoard Interrupt')
            server.shutdown()
