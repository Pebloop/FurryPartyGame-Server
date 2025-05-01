#!/usr/bin/env python

import asyncio
import json
import os
import signal
import ssl

from websockets import ConnectionClosedOK
from websockets.asyncio.server import serve, ServerConnection
from dotenv import load_dotenv

from src.data import get_connection, get_game, set_game
from src.manage_websockets import manage_websockets


async def on_connection_closed(websocket):
    closed = get_connection(websocket)

    if closed is not None:
        if closed["type"] == "game":
            for player in get_game(closed["game_key"])["players"]:
                await player["client"].send(json.dumps({"type": "game_closed"}))
        elif closed["type"] == "player":
            print(f"Player {closed['name']} left the game")
            game = get_game(closed["game_key"])
            game["players"] = [player for player in game["players"] if player["name"] != closed["name"]]
            set_game(closed["game_key"], game)
            await game["client"].send(json.dumps({"type": "player_left", "player": closed["name"]}))

    await websocket.close()


async def handler(websocket: ServerConnection):
    # add listener for connection closed
    closed = asyncio.ensure_future(websocket.wait_closed())
    closed.add_done_callback(lambda _: asyncio.ensure_future(on_connection_closed(websocket)))

    try:
        async for message in websocket:
            await manage_websockets(message, websocket)
    except ConnectionClosedOK:
        await on_connection_closed(websocket)


async def main():
    load_dotenv()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(os.getenv("SSL_FULLCHAIN", ""), os.getenv("SSL_PRIVKEY", ""))
    port = int(os.getenv("PORT", 8001))

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(handler, os.getenv("HOST", "localhost"), port, ssl=ssl_context):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
