import asyncio
import websockets

from root.side_modules.settings import *

async def handler(websocket):
    print('Connection added...')
    await websocket.send('Hello User!')
    async for message in websocket:
        print(message)

async def main():
    async with websockets.serve(handler, HOST, WS_PORT):
        await asyncio.Future()  # run forever
