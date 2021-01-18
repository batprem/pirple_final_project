"""
Author Prem
Description:
	- Pirple.com final project for the Python course.
	- Making online card game where the selected game is PokDeng
Reference:
	- https://en.wikipedia.org/wiki/Pok_Deng
"""

import copy
from flask import Flask, request
from Casino import *

challengeTable = {}
app = Flask(__name__)

table: Table
Endgame = 2


def get_score(player_id):
	"""

	:param player_id: get player score
	"""
	score, pok, deng = casino.table.score_master.cal_score(casino.players[player_id].cards_on_hands)
	casino.players[player_id].score['score'] = score
	casino.players[player_id].score['pok'] = pok
	casino.players[player_id].score['deng'] = deng
	casino.table.score_master.is_pok = pok


@app.route("/player-register", methods=["POST"])
def register_player():
	"""
	Register player to server
	:return: server_text, player_id
	"""
	json_data = request.json
	player_name = json_data.get('player_name')
	player_credits = json_data.get('credits')
	player = Player(name=player_name, player_credits=player_credits)
	player_id = len(casino.players)
	casino.players.append(player)

	return {
		"server_text": f"Welcome {player_name}! Your id is {player_id}",
		"player_id": player_id
	}


@app.route("/get-players", methods=["POST"])
def get_players():
	"""
	Get players online
	:return: {
		"server_text": (str)
		"players" (json)
	}
	"""
	return {
		"server_text": "Here are players are in our casino",
		"players": {i: player.name for i, player in enumerate(casino.players)}
	}


@app.route("/challenges-a-player", methods=["POST"])
def challenges_a_player():
	"""
	Allow players to challenge another
	:return:
	"""
	json_data = request.json
	player_id = json_data.get('player_id')
	challenged_player_id = json_data.get('challenged_player_id')
	if player_id >= 0 and challenged_player_id >= 0:
		if player_id == challenged_player_id:
			return {
				"server_text": "You can't challenge yourself"
			}
		challengeTable[int(player_id)] = int(challenged_player_id)

		return {
			"server_text": "Your challenge has been placed. Wait for responses"
		}


@app.route("/check-challenge-table", methods=["POST"])
def check_challenge_table():
	"""
	Check whether there are players challenging him/her or not
	:return:  server_text, challenge_list (if there are)
	"""
	json_data = request.json
	player_id = json_data.get('player_id')
	print(challengeTable)
	if player_id >= 0:
		# Seeking
		challenges_to_player = [
			challenger
			for challenger, challenged
			in challengeTable.items()
			if challenged == player_id
		]
		if challenges_to_player:
			challenge_list = {
				int(challenger_id): casino.players[challenger_id].name
				for challenger_id
				in challenges_to_player
			}
			return {
				"server_text": "choose one of these players",
				"challenge_list": challenge_list
			}
		else:
			return {
				"server_text": "No one challenge you yet"
			}


@app.route("/response-to-challenge", methods=["POST"])
def response_to_challenge():
	"""
	Player accept a challenge
	:return: server_text, start_game
	"""
	global table
	json_data = request.json
	player_id = json_data.get('player_id')
	accept_id = json_data.get('accept_id')

	if (accept_id in challengeTable) and (challengeTable[accept_id] == player_id):
		casino.table = Table(casino.players[player_id], casino.players[accept_id])
		casino.deck = Deck()  # Initial deck
		casino.deck.shuffle()  # Shuffle
		# Player 1 Draw 2 cards
		casino.players[player_id].draw_a_card(casino.deck)
		casino.players[player_id].draw_a_card(casino.deck)
		get_score(player_id)
		# Player 2 Draw 2 cards
		casino.players[accept_id].draw_a_card(casino.deck)
		casino.players[accept_id].draw_a_card(casino.deck)
		get_score(accept_id)
		# Set player 1 turn
		casino.table.player_1.is_player_turn = True
		casino.players[player_id].endgame = False
		casino.players[accept_id].endgame = False

		return {"server_text": "Let's play!", "start_game": True}
	else:
		return {"server_text": "Invalid challenge id", "start_game": False}


@app.route("/check-players-accept-challenge", methods=["POST"])
def check_players_accept_challenge():
	"""
	Check whether player accepted challenge
	:return: server_text, start_game
	"""
	json_data = request.json
	player_id = json_data.get('player_id')

	try:
		if casino.table.player_2.id == player_id:
			return {"server_text": "Let's play!", "start_game": True}
		else:
			return {"server_text": "Player not found or didn't challenge you yet", "start_game": False}
	except AttributeError:
		return {"server_text": "Keep waiting", "start_game": False}


@app.route("/get-player-status", methods=["POST"])
def get_player_status():
	"""
	Check whether player accepted challenge
	:return: server_text, start_game
	"""
	json_data = request.json
	player_id = json_data.get('player_id')
	the_player = casino.players[player_id]
	returning_data = copy.copy(the_player.__dict__)

	cards_on_hands_dict = [card.__dict__ for card in the_player.cards_on_hands]
	returning_data['cards_on_hands'] = cards_on_hands_dict
	try:
		returning_data['opponent'] = casino.table.opponent[player_id]
	except AttributeError:
		pass
	return returning_data


@app.route("/player-play", methods=["POST"])
def player_play():
	"""
	Player play turn
	:return: server_text, start_game
	"""
	global Endgame
	json_data = request.json
	player_id = json_data.get('player_id')
	action = json_data.get('action')

	score, pok, deng = casino.table.score_master.cal_score(casino.players[player_id].cards_on_hands)
	casino.players[player_id].score['score'] = score
	casino.players[player_id].score['pok'] = pok
	casino.players[player_id].score['deng'] = deng
	casino.table.score_master.is_pok = pok

	if action == 'draw':
		if casino.table.score_master.is_pok:
			casino.players[player_id].draw_a_card(casino.deck)
			server_text = "Draw another card"
		else:
			server_text = "Some player get pok! Can't draw a new card"

	elif action == 'skip':
		server_text = "Skip your turn"
	else:
		server_text = ""

	casino.players[player_id].is_player_turn = False
	opponent_id = casino.table.opponent[player_id]['id']
	casino.players[opponent_id].is_player_turn = True

	Endgame -= 1
	if Endgame:
		return {
			"server_text": server_text
		}
	else:
		if casino.players[player_id].score['score'] > casino.players[opponent_id].score['score']:
			casino.players[player_id].win = True
			bet = casino.players[player_id].score['deng']*100
			casino.players[player_id].credits += bet
			casino.players[opponent_id].credits -= bet

		elif casino.players[player_id].score['score'] < casino.players[opponent_id].score['score']:
			casino.players[opponent_id].win = True
			bet = casino.players[opponent_id].score['deng'] * 100
			casino.players[opponent_id].credits += bet
			casino.players[player_id].credits -= bet

		else:
			if casino.players[player_id].score['deng'] >= casino.players[opponent_id].score['deng']:
				casino.players[player_id].win = True
				bet = casino.players[player_id].score['deng'] * 100
				casino.players[player_id].credits += bet
				casino.players[opponent_id].credits -= bet
			else:
				casino.players[opponent_id].win = True
				bet = casino.players[opponent_id].score['deng'] * 100
				casino.players[opponent_id].credits += bet
				casino.players[player_id].credits -= bet
		casino.players[player_id].cards_on_hands = []
		casino.players[opponent_id].cards_on_hands = []
		casino.players[player_id].endgame = True
		casino.players[opponent_id].endgame = True
		return {
			"server_text": "Game over"
		}


@app.route("/reset-challenge", methods=["POST"])
def reset_challenge():
	"""
	Reset to initial state
	:return: server_text, start_game
	"""
	global Endgame
	global challengeTable
	challengeTable = {}
	try:
		del casino.table
	except AttributeError:
		pass
	Endgame = 2

	return {
		"server_text": "Table is reset"
	}


if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0', threaded=True)
	except KeyboardInterrupt:
		raise
