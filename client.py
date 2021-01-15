"""
Author: Prem
For players to connect to server and play the game
"""

import json
import requests

HEADERS = {
    'Content-Type': 'application/json'
}

base_url = "http://127.0.0.1:5000"


def register_player(player_name, player_credits):
    """

    :param player_name:
    :param player_credits:
    :return:
    """
    url = f"{base_url}/player-register"

    payload = json.dumps({
        "player_name": player_name,
        "credits": player_credits
    }
    )

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    return response.json()


def get_players():
    """

    :return:
    """
    url = f"{base_url}/get-players"

    payload = json.dumps({})

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    return response.json()


def check_challenge_table(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/check-challenge-table"

    payload = json.dumps(params)

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    return response.json()
