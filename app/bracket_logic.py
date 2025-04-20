import uuid
import math

class Match:
	def __init__(self, player1=None, player2=None):
		self.player1 = player1
		self.player2 = player2
		self.score1 = None
		self.score2 = None
		self.winner = None

class Bracket:
	def __init__(self, participants):
		self.participants = participants[:]
		if len(self.participants) % 2 != 0:
			self.participants.append(None)

		self.rounds = []  # rounds[round_index][match_index]
		self._build()

	def _build(self):
		current_players = self.participants
		num_matches = len(current_players) // 2

		# Round 1
		round_matches = []
		for i in range(0, len(current_players), 2):
			round_matches.append(Match(current_players[i], current_players[i+1]))
		self.rounds.append(round_matches)

		# Future rounds
		while num_matches > 1:
			num_matches = math.ceil(num_matches / 2)
			self.rounds.append([Match() for _ in range(num_matches)])

	def __getitem__(self, index):
		round_num, match_num = index
		return self.rounds[round_num - 1][match_num - 1]