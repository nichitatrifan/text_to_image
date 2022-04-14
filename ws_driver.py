import asyncio

from root.websockets.app import main

if __name__ == "__main__":
    print('WS is being listened on: ' + '127.0.0.1:5051')
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
            print('KeyboardInterrupt')