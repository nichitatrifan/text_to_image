from root.side_modules.settings import *

class Router:
    def __init__(self, *a, **kw):
        self.conf_args = a
        self.conf_kw = kw

    def __call__(self, *args, **kw):
        ROUTE_MAP[self.conf_args[0]] = args[0]
        print(ROUTE_MAP)

if __name__ == '__main__':
    pass