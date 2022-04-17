import asyncio
import websockets
import threading

from root.side_modules.settings import *

async def handler(websocket):
    print('Connection added...')
    await websocket.send('Hello User!')
    async for message in websocket:
        print(message)

async def main():
    async with websockets.serve(handler, HOST, WS_PORT):
        await asyncio.Future()  # run forever

def start_ws():
    print('WS is being listened on: ' + '127.0.0.1:5051')
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
            print('KeyboardInterrupt')
            threading.current_thread().join()

if __name__ == "__main__":
    pass