import uuid
import math

class Match:
	def __init__(self, player1=None, player2=None, round_index=0, match_index=0):
		self.player1 = player1
		self.player2 = player2
		self.score1 = None
		self.score2 = None
		self.winner = None
		self.round_index = round_index
		self.match_index = match_index
		self.x = round_index
		self.y = None  # to be set later
		self.feeders = []

	def set_feeders(self, match1, match2):
		self.feeders = [match1, match2]
		self.y = (match1.y + match2.y) / 2 if match1 and match2 else match1.y if match1 else 0

class Bracket:
	def __init__(self, participants):
		self.participants = participants[:]
		if len(self.participants) % 2 != 0:
			self.participants.append(None)

		self.rounds = []  # 2D: rounds[round][match]
		self.all_matches = []
		self._build()

	def _build(self):
		# Round 1: create actual matches
		num_matches = len(self.participants) // 2
		round_0 = []
		for i in range(num_matches):
			p1 = self.participants[i * 2]
			p2 = self.participants[i * 2 + 1]
			match = Match(p1, p2, round_index=0, match_index=i)
			match.y = i * 4  # even spacing
			round_0.append(match)
			self.all_matches.append(match)
		self.rounds.append(round_0)

		# Future rounds
		current_round = round_0
		round_index = 1
		while len(current_round) > 1:
			next_round = []
			for i in range(0, len(current_round), 2):
				m1 = current_round[i]
				m2 = current_round[i + 1] if i + 1 < len(current_round) else None
				match = Match(round_index=round_index, match_index=i // 2)

				# Set feeder matches so y is calculated properly
				if m2:
					match.set_feeders(m1, m2)
				else:
					match.y = m1.y  # carry forward

				next_round.append(match)
				self.all_matches.append(match)
			self.rounds.append(next_round)
			current_round = next_round
			round_index += 1
			
	def debug_print(self):
		print("\n--- Bracket Structure ---")
		for round_num, matches in enumerate(self.rounds):
			print(f"Round {round_num + 1}:")
			for m in matches:
				p1 = m.player1.name if m.player1 else "None"
				p2 = m.player2.name if m.player2 else "None"
				print(f"  Match: {p1} vs {p2} | x={m.x}, y={m.y}")
		print("--- End Bracket ---\n")