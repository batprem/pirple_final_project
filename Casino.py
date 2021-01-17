"""
Casino object
"""
import random
from collections import Counter

players = []


class Card:
	"""
	just cards
	:param pips: '♣', '♦', '♥', '♠'
	:param index: 'A', 1, 2, ... J, Q,K
	"""

	def __init__(self, pips, index):
		index = str(index)
		self.pips = pips
		self.index = index
		self.indices = index

	def __add__(self, card):
		if self.index == 'A':
			card_1_score = 1
		elif self.index in ['J', 'Q', 'K']:
			card_1_score = 0
		else:
			card_1_score = int(self.index)

		if card.index == 'A':
			card_2_score = 1
		elif card.index in ['J', 'Q', 'K']:
			card_2_score = 0
		else:
			card_2_score = int(card.index)
		point = (card_1_score + card_2_score) % 10
		deng = (self.pips + card.pips)
		commutative_score = self.__class__(deng, point)
		commutative_score.indices = self.index + card.index
		commutative_score.indices.replace('1', 'A')
		return commutative_score

	def __repr__(self):
		return str(self.__dict__)


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
		self.is_player_turn = False
		self.win = False
		self.status = ''
		self.score = {}

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

	def __init__(self, player_1: Player, player_2: Player):
		self.player_1 = player_1
		self.player_2 = player_2
		self.is_pok = False
		pass

	@staticmethod
	def check_sam_lueang(sum_score):
		"""

		:param sum_score:
		:return: return if cards are Sam Lueang
		"""
		indices_list = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
		for index in range(11):
			if all([i in sum_score.indices for i in indices_list[index: index + 3]]):
				return True
		return False

	def check_deng(self, sum_score):
		"""
		Return deng score
		:param sum_score:
		:return:
		"""
		len_pips = len(sum_score.pips)
		deng = 1
		pok = False
		if len_pips == 2:
			# Check pok
			if int(sum_score.index) >= 8:
				pok = True
				if list(Counter(sum_score.indices).values())[0] == 2:
					deng = 2
			elif list(Counter(sum_score.pips).values())[0] == 2:
				deng = 2

		elif len_pips == 3:
			# Check Tong
			if list(Counter(sum_score.indices).values())[0] == 3:
				deng = 5
			# Check sam lueang
			elif self.check_sam_lueang(sum_score):
				deng = 3
		return pok, deng

	def cal_score(self, cards_on_hands):
		"""
		Calcucalate score
		:param cards_on_hands:
		:return score (int), deng (int)
		"""
		sum_score = sum(cards_on_hands, Card('', 0))
		pok, deng = self.check_deng(sum_score)
		score = sum_score.index
		return score, pok, deng


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
		self.score_master = ScoreMaster(self.player_1, self.player_2)
		self.opponent = {
			player_1.id: {
				"id": player_2.id,
				"name": player_2.name
			},
			player_2.id: {
				"id": player_1.id,
				"name": player_1.name
			},
		}


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
