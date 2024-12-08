import json
import secrets


def manage_websockets(message: str, websocket):
    # convert to json
    try:
        message_json = json.loads(message)
    except json.JSONDecodeError:
        print("Invalid WebSocket message : not a valid JSON")
        return

    eventType = message_json.get("type")

    if eventType == "init":
        game = message_json.get("game")
        game_key = secrets.token_urlsafe(6)
        print(f"New game created with key {game_key}")
        websocket.send(json.dumps({"type": "init", "game_key": game_key}))
