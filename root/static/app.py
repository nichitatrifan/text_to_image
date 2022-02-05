#!/usr/bin/env python

import asyncio

import websockets

# handler that manages each connection
async def handler(websocket):
    async for message in websocket:
        print(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
            print('KeyboardInterrupt')