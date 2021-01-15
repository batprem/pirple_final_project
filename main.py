"""
Author Prem
Description:
	- Pirple.com final project for the Python course.
	- Making online card game where the selected game is PokDeng
Reference:
	- https://en.wikipedia.org/wiki/Pok_Deng
"""

from flask import Flask, request
from Casino import Casino

casio = Casino()
challengeTable = {}
app = Flask(__name__)

table: Casino.Table


@app.route("/player-register", methods=["POST"])
def register_player():
	"""
	Register player to server
	:return: server_text, player_id
	"""
	json_data = request.json
	player_name = json_data.get('player_name')
	player_credits = json_data.get('credits')
	player = Casino.Player(name=player_name, player_credits=player_credits)
	player_id = len(casio.players)
	casio.players.append(player)

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
		"server_text": "Here are players are in our casio",
		"players": {i: player.name for i, player in enumerate(casio.players)}
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
				int(challenger_id): casio.players[challenger_id].name
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
		table = casio.Table(casio.players[player_id], casio.players[accept_id])
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

	if table.player_2.id == player_id:
		return {"server_text": "Let's play!", "start_game": True}
	else:
		return {"server_text": "Keep waiting", "start_game": False}


if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0', threaded=True)
	except KeyboardInterrupt:
		raise