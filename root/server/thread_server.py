import socketserver

import root.side_modules.settings as st

from root.server.logger import Logger


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, Logger):
    #TODO create a function for the active connections displaying
    # use that function as a separate thread
    def __init__(self, *args) -> None:
        Logger.__init__(self)
        super().__init__(*args)
    
    def signal_shut_down(self):
        st.SHUT_DOWN_SERVER = True


if __name__ == "__main__":
    pass