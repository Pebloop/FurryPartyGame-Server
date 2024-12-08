import json


def manage_websockets(message: str):
    # convert to json
    try:
        message_json = json.loads(message)
    except json.JSONDecodeError:
        print("Invalid WebSocket message : not a valid JSON")
        return

    eventType = message_json.get("type")

    if eventType == "init":
        game = message_json.get("game")
        print(f"Game {game} initialized")
