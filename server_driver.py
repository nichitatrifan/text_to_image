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

            while server_thread.is_alive():
                server_thread.join(1.0) # waits until the thread terminates
                server.logger.info(f'ACTIVE CONNECTIONS {threading.active_count() - 1}')

        except KeyboardInterrupt as kyi:
            # join all the threads on the server!
            server.logger.warning('KeyBoard Interrupt')
            server.signal_shut_down()
            server.shutdown()
            