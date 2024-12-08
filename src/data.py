from typing import Any, Dict

DATA: Dict[str, Any] = {}


def set_game(game_key: str, game) -> None:
    DATA[game_key] = game


def get_game(game_key: str):
    return DATA.get(game_key)


def remove_game(game_key: str):
    DATA.pop(game_key)


def does_game_exist(game_key: str):
    return game_key in DATA
