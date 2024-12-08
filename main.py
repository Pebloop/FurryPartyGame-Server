#!/usr/bin/env python

import asyncio
import os
import ssl

from websockets import ConnectionClosedOK
from websockets.asyncio.server import serve
from dotenv import load_dotenv

from src.manage_websockets import manage_websockets

async def handler(websocket):
    async for message in websocket:
        await manage_websockets(message, websocket)


async def main():
    load_dotenv()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(os.getenv("SSL_FULLCHAIN", ""), os.getenv("SSL_PRIVKEY", ""))
    port = int(os.getenv("PORT", 8001))
    async with serve(handler, os.getenv("HOST", "localhost"), port, ssl=ssl_context):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
