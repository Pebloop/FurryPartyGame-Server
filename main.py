#!/usr/bin/env python

import asyncio
import json
import os
import ssl

from websockets import ConnectionClosedOK
from websockets.asyncio.server import serve
from dotenv import load_dotenv

from src.data import get_connection, get_game
from src.manage_websockets import manage_websockets


async def on_connection_closed(websocket):
    closed = get_connection(websocket)

    if closed is not None:
        if closed["type"] == "game":
            print(f"Game {closed['game_key']} closed")
            for player in get_game(closed["game_key"])["players"]:
                await player["client"].close(reason=ConnectionClosedOK)
        elif closed["type"] == "player":
            print(f"Player {closed['name']} left the game")
            game = get_game(closed["game_key"])
            game["players"].remove(closed["name"])
            game["client"].send(json.dumps({"type": "player_left", "name": closed["name"]}))

    await websocket.close()


async def handler(websocket, path):
    closed = asyncio.ensure_future(websocket.wait_closed())
    closed.add_done_callback(on_connection_closed)

    async for message in websocket:
        await manage_websockets(message, websocket)


async def main():
    load_dotenv()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(os.getenv("SSL_FULLCHAIN", ""), os.getenv("SSL_PRIVKEY", ""))
    port = int(os.getenv("PORT", 8001))
    async with serve(handler, os.getenv("HOST", "localhost"), port, ssl=ssl_context):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
