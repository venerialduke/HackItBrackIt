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
		if match1 and match2:
			self.y = (match1.y + match2.y) / 2
		elif match1:
			self.y = match1.y
		else:
			self.y = 0

class Bracket:
	def __init__(self, participants, match_results=None):
		# Store match results (if any) from e.g. session
		self.match_results = match_results or {}
		self.participants = participants[:]
		# If odd number, pad with a None
		if len(self.participants) % 2 != 0:
			self.participants.append(None)

		self.rounds = []  # 2D list: rounds[round][match]
		self.all_matches = []
		self._build()

	def _build(self):
		# Build Round 0 from the participants.
		num_matches = len(self.participants) // 2
		round_0 = []
		for i in range(num_matches):
			p1 = self.participants[i * 2]
			p2 = self.participants[i * 2 + 1]
			match = Match(p1, p2, round_index=0, match_index=i)
			match.y = i * 4  # even spacing
			# If there is a saved result, update the match.
			key = f"r0_m{i}"
			if key in self.match_results:
				result = self.match_results[key]
				match.score1 = result["score1"]
				match.score2 = result["score2"]
				if result["winner"] == "player1":
					match.winner = p1
				elif result["winner"] == "player2":
					match.winner = p2
			round_0.append(match)
			self.all_matches.append(match)
		self.rounds.append(round_0)

		# Build subsequent rounds until only one match remains.
		current_round = round_0
		round_index = 1
		while len(current_round) > 1:
			next_round = []
			for i in range(0, len(current_round), 2):
				m1 = current_round[i]
				m2 = current_round[i + 1] if i + 1 < len(current_round) else None
				match = Match(round_index=round_index, match_index=i // 2)
				# Use feeder matches to calculate vertical position.
				if m2:
					match.set_feeders(m1, m2)
				else:
					match.y = m1.y  # single match carries forward

				# Set players based on feeders’ winners, if available.
				if m1 and m1.winner:
					match.player1 = m1.winner
				if m2 and m2.winner:
					match.player2 = m2.winner

				# Check if a score has been submitted for this match.
				key = f"r{round_index}_m{match.match_index}"
				if key in self.match_results:
					result = self.match_results[key]
					match.score1 = result["score1"]
					match.score2 = result["score2"]
					if result["winner"] == "player1":
						match.winner = match.player1
					elif result["winner"] == "player2":
						match.winner = match.player2

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
				print(f"  Match: {p1} vs {p2} | x={m.x}, y={m.y}, "
				      f"Score: {m.score1} - {m.score2}, Winner: {m.winner.name if m.winner else 'None'}")
		print("--- End Bracket ---\n")