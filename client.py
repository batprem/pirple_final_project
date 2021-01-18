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


def get_player_status(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/get-player-status"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def player_play(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/player-play"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def reset_challenge(**params):
    """

    :param params:
    :return:
    """
    url = f"{base_url}/reset-challenge"
    payload = json.dumps(params)
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def show_help():
    """

    :return: True
    """
    print("""1. The players place their bets.
2. The dealer shuffles and deals two cards to each player, ending with the dealer.
3. Each player may stay or draw one card.
4. The dealer may compare his or her hand against select players.
5. The dealer may draw a card.
6. The dealer compares his or her hand against the rest of the players.
checkout: https://en.wikipedia.org/wiki/Pok_Deng for more information
""")
    resume = 'x'
    while resume != '--resume':
        resume = input("Type `--resume to continue the game")
    return True


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
        return lobby_state()


# State 1: Registering
player = Player(input("Please enter player name: "), int(input("How much money do you have?: ")))
register_response = register_player(player.name, player.credits)
print(register_response["server_text"])
player.id = register_response['player_id']
while True:
    # State 2: In the Lobby
    next_stage = lobby_state()
    # State 2.1: Waiting for challenge accept
    if next_stage == 'Waiting for challenge accept':
        start_game = waiting_for_challenge_accept()
    # State 2.2: Waiting for challenge
    if next_stage == 'Waiting for challenge':
        start_game = waiting_for_challenge()

    # Stage 3 Playing
    # Stage 3.1 first round
    while True:
        player_status = get_player_status(player_id=player.id)
        opponent = player_status['opponent']
        player_turn = player_status['is_player_turn']
        cards_on_hands = player_status['cards_on_hands']
        print("Your cards")
        for card in cards_on_hands:
            print(f"Pip: {card['pips']}")
            print(f"Index: {card['index']}")
            print('-'*36)
        if player_turn:
            print(f"{player.name}'s turn")
            print(f"Please select 1 of these 3 options")
            print(" - `draw` to draw another card")
            print(" - `skip` to skip this turn")
            print(" - `--help` to print help`")
            option = input(">>> ")
            if option == '--help':
                show_help()
            elif option in ['draw', 'skip']:
                player_play_response = player_play(player_id=player.id, action=option)
                print(player_play_response)

                # Get player status
                player_status = get_player_status(player_id=player.id)
                opponent = player_status['opponent']
                player_turn = player_status['is_player_turn']
                cards_on_hands = player_status['cards_on_hands']
                print("Your cards")
                for card in cards_on_hands:
                    print(f"Pip: {card['pips']}")
                    print(f"Index: {card['index']}")
                    print('-' * 36)
                break
            else:
                continue
        else:
            print(f"{opponent['name']}'s turn")
            print("Please wait")
        time.sleep(5)

    # Stage 4: Calculate score
    print("Wait for another's play")
    while True:
        player_status = get_player_status(player_id=player.id)
        if player_status.get('endgame'):
            break
    if player_status['win']:
        print(f"{player_status['name']} WIN!")
        print(f"Your current credit's {player_status['credits']}")
    else:
        print(f"{opponent['name']} WIN!")
        print(f"Your current credit's {player_status['credits']}")

    print(f"Your score is {player_status['score']}")

    print(reset_challenge())