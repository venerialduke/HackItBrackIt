import uuid
import math

class Match:
	def __init__(self, player1=None, player2=None, round_index=0, match_index=0):
		self.player1 = player1
		self.player2 = player2
		self.score1 = None
		self.score2 = None
		self.winner = None
		self.round_index = round_index  # x axis
		self.match_index = match_index  # index in round
		self.y = None  # vertical position
		self.x = round_index
		self.feeders = []

	def set_feeders(self, match1, match2):
		self.feeders = [match1, match2]
		self.y = (match1.y + match2.y) / 2

class Bracket:
	def __init__(self, participants):
		self.participants = participants[:]
		if len(self.participants) % 2 != 0:
			self.participants.append(None)

		self.rounds = []  # 2D: rounds[round][match]
		self.all_matches = []
		self._build()

	def _build(self):
		# Round 1
		num_matches = len(self.participants) // 2
		round_0 = []
		for i in range(num_matches):
			p1 = self.participants[i*2]
			p2 = self.participants[i*2 + 1]
			match = Match(p1, p2, round_index=0, match_index=i)
			match.y = i * 4  # vertical spacing step
			round_0.append(match)
			self.all_matches.append(match)
		self.rounds.append(round_0)

		# Later rounds
		current_round = round_0
		round_index = 1
		while len(current_round) > 1:
			next_round = []
			for i in range(0, len(current_round), 2):
				m1 = current_round[i]
				m2 = current_round[i+1] if i+1 < len(current_round) else None
				match = Match(round_index=round_index, match_index=i//2)
				if m2:
					match.set_feeders(m1, m2)
				else:
					match.y = m1.y  # carry forward y
				next_round.append(match)
				self.all_matches.append(match)
			self.rounds.append(next_round)
			current_round = next_round
			round_index += 1