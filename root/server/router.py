#TODO create a router
# a class that is going to map 
# its functions with the endpoints

from root.side_modules.settings import *

class Router:
    def __init__(self, *a, **kw):
        self.conf_args = a
        self.conf_kw = kw

    def __call__(self, *args, **kwds):
        ROUTE_MAP[args[0].__name__] = args[0]
        print(ROUTE_MAP)

if __name__ == '__main__':
    pass