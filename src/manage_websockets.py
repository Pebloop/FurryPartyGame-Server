import json
import secrets

from src.data import does_game_exist, set_game


def generate_room_key():
    return secrets.token_urlsafe(4).upper()


async def manage_websockets(message: str, websocket):
    # convert to json
    try:
        message_json = json.loads(message)
    except json.JSONDecodeError:
        print("Invalid WebSocket message : not a valid JSON")
        return

    eventType = message_json.get("type")

    if eventType == "init":
        await event_init(message_json, websocket)
    if eventType == "join":
        await event_join(message_json, websocket)


async def event_init(message_json, websocket):
    game = message_json.get("game")
    game_key = generate_room_key()
    while does_game_exist(game_key):
        game_key = generate_room_key()
    print(f"New game created with key {game_key}")
    set_game(game_key, {"game": game, "players": []})
    await websocket.send(json.dumps({"type": "room_key", "game_key": game_key}))


async def event_join(message_json, websocket):
    game_key = message_json.get("game_key")
    print(f"Player joined game with key {game_key}")
