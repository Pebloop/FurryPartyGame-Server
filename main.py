#!/usr/bin/env python

import asyncio

from websockets import ConnectionClosedOK
from websockets.asyncio.server import serve

from src.manage_websockets import manage_websockets


async def handler(websocket):
    async for message in websocket:
        await manage_websockets(message, websocket)


async def main():
    async with serve(handler, "ws-fpg.pebloop.dev", 8001):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
