import asyncio
import websockets

import root.side_modules.settings as st

# handler that manages each connection
async def handler(websocket):    
    await websocket.send('Hello User!')
    async for message in websocket:
        print(message)


async def main():
    async with websockets.serve(handler, "", st.PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
            print('KeyboardInterrupt')