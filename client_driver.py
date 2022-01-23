'''Driver Code'''
import sys

from root.client.sender import Sender

def main():
    #s = Sender(('localhost', 9999))
    s = Sender(('localhost', 5050))
    # s.key_exchange(key)
    s.key_exchange()
    s.save_char_map()
    s.close()


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print(f'Usage: {sys.argv[0]}')
    #     sys.exit(-1)
    # if sys.argv[1] in ('-h', '--help'):
    #     print(f'Usage: {sys.argv[0]}')
    #     sys.exit(0)
    #main(sys.argv[1])
    main()
