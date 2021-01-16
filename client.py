"""
Author: Prem
For players to connect to server and play the game
"""

from Casino import Player
import json
import requests
import time

HEADERS = {
    'Content-Type': 'application/json'
}

base_url = "http://127.0.0.1:5000"


class Interrupt(BaseException):
    """
    Help interuption
    """
    pass


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


def challenge_a_player(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/challenges-a-player"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def response_to_challenge(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/response-to-challenge"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def check_players_accept_challenge(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/check-players-accept-challenge"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


# State 1: Registering
player = Player(input("Please enter player name: "), int(input("How much money do you have?: ")))
register_response = register_player(player.name, player.credits)
print(register_response["server_text"])
player.id = register_response['player_id']


# State 2: In the Lobby
def lobby_state():
    """

    :return: (str) next stage
    """

    player_response = get_players()
    print(player_response['server_text'])
    for player_id, player_name in player_response['players'].items():
        print(f'Id: {player_id}| Name: {player_name}')

    challenge_id = input("Type player id of who you want challenge or type `wait` for wait challenge")
    if challenge_id in player_response['players']:
        print(f"You're challenging {player_response['players'][challenge_id]}. Wait for him/her to response")
        print(challenge_a_player(player_id=player.id, challenged_player_id=int(challenge_id)))
        return 'Waiting for challenge accept'

    elif challenge_id == 'wait':
        return 'Waiting for challenge'

    else:
        print("Player id not found")


next_stage = lobby_state()
# State 2.1: Waiting for challenge accept
if next_stage == 'Waiting for challenge accept':
    def waiting_for_challenge_accept():
        """

        :return:
        """

        print("waiting for accept")
        while True:
            acceptance = check_players_accept_challenge(player_id=int(player.id))
            print(acceptance['server_text'])
            if acceptance['start_game']:
                return acceptance['start_game']
            time.sleep(5)

    start_game = waiting_for_challenge_accept()
# State 2.2: Waiting for challenge
if next_stage == 'Waiting for challenge':
    def waiting_for_challenge():
        """

        :return:
        """

        print("waiting for challenge")
        while True:
            challenge_res = check_challenge_table(player_id=player.id)
            print(challenge_res)
            if 'challenge_list' in challenge_res:
                # Found challenge
                challenge_list = challenge_res['challenge_list']
                challenge_id = input(challenge_res['server_text'])
                if challenge_id in challenge_list:
                    print(f"You accepted challenge from {challenge_list[challenge_id]}")
                    challenge_response = response_to_challenge(player_id=int(player.id), accept_id=int(challenge_id))
                    print(challenge_response['server_text'])
                    start = challenge_response['start_game']
                    if start:
                        return start
            time.sleep(5)


    start_game = waiting_for_challenge()
