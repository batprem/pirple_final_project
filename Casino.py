"""
Casino object
"""
import random

players = []


class Card:
	"""
	just cards
	:param pips: '♣', '♦', '♥', '♠'
	:param index: 'A', 1, 2, ... J, Q,K
	"""

	def __init__(self, pips, index):
		self.pips = pips
		self.index = index


class Deck:
	"""
	decks, group of cards
	"""

	def __init__(self):
		self.cards = []
		for pips in ['♣', '♦', '♥', '♠']:
			for index in range(1, 14):
				if index == 1:
					card = Card(pips, 'A')
				elif index == 11:
					card = Card(pips, 'J')
				elif index == 12:
					card = Card(pips, 'Q')
				elif index == 13:
					card = Card(pips, 'K')
				else:
					card = Card(pips, str(index))
				self.cards.append(card)
		self.amount_of_cards = len(self.cards)

	def shuffle(self):
		"""
		Shuffle deck
		"""
		random.shuffle(self.cards)

	def give_a_card(self):
		"""
		Give a card to a player when he/she draws
		:return: card
		"""
		card = self.cards[0]
		self.amount_of_cards -= 1
		self.cards = self.cards[1:]
		return card


class Player:
	"""
	Players in casino
	"""

	def __init__(self, name: str, player_credits: int):
		self.id = len(casino.players)
		self.name = name
		self.cards_on_hands = []
		self.credits = player_credits

	def draw_a_card(self, playing_deck):
		"""
		Pick a deck and draw a card
		:param playing_deck: (Deck)
		"""
		self.cards_on_hands.append(playing_deck.give_a_card())


class ScoreMaster:
	"""
	Who runs a game and controls rule
	"""

	def __init__(self):
		pass


class Table:
	"""
	Where players play a game
	"""

	def match_player(self):
		"""
		Match and start the game
		"""
		print(f"Match making between {self.player_1.name} and {self.player_2.name}")

	def __init__(self, player_1, player_2):
		# Match player
		self.player_1 = player_1
		self.player_2 = player_2
		self.deck = Deck()
		print(f"Match making between {self.player_1.name} and {self.player_2.name}")
		self.match_player()
		self.score_master = ScoreMaster()


class Casino:
	"""
	Everything a casino need to have
	"""

	def __init__(self):
		self.players = []
		pass

	def add_a_player(self, new_player):
		"""
		Add new player to the casino
		:param new_player:
		"""

		players.append(new_player)
		self.players = new_player


casino = Casino()
