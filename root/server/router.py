from root.side_modules.settings import *
from root.server.logger import Logger

class Router(Logger):
    def __init__(self, *a, **kw):
        self.conf_args = a
        self.conf_kw = kw
        Logger.__init__(self)

    def __call__(self, *args, **kw):
        ROUTE_MAP[self.conf_args[0]] = args[0]
        self.logger.info('ENDPOINT: ' + str(self.conf_args[0]))

if __name__ == '__main__':
    pass
