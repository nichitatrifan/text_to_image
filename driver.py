'''Driver Code'''

import sys

from sender import Sender
from receiver import Receiver

def main(key):
    s = Sender(('localhost', 9999))
    s.key_exchange(key)
    s.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]}')
        sys.exit(-1)
    if sys.argv[1] in ('-h', '--help'):
        print(f'Usage: {sys.argv[0]}')
        sys.exit(0)
    main(sys.argv[1])
