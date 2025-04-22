from flask import render_template, request, redirect, url_for, session
from .models import Participant
from .bracket_logic import Bracket
from . import db
from flask import Blueprint

bp = Blueprint('main', __name__)  # <- this is the blueprint object

@bp.route('/', methods=['GET', 'POST'])
def register():
	print("Inside route!")  # temp debug
	if request.method == 'POST':
		name = request.form['name']
		color = request.form['color']
		show = request.form['show']
		avatar_filename = generate_avatar_filename(name, color, show)

		new_participant = Participant(
			name=name,
			favorite_color=color,
			favorite_show=show,
			avatar_filename=avatar_filename
		)
		db.session.add(new_participant)
		db.session.commit()
		return redirect(url_for('main.register'))

	participants = Participant.query.all()
	return render_template('register.html', participants=participants)

@bp.route('/remove_participant', methods=['POST'])
def remove_participant():
	participant_id = request.form.get('participant_id')
	if participant_id:
		participant = Participant.query.get(participant_id)
		if participant:
			db.session.delete(participant)
			db.session.commit()
	return redirect(url_for('main.register'))

def generate_avatar_filename(name, color, show):
	index = (hash(name + color + show) % 8) + 1
	return f'avatar{index}.png'

@bp.route('/bracket', methods=['GET'])
def bracket():
	participants = Participant.query.all()
	# Get stored match results from session
	match_results = session.get("match_results", {})
	bracket = Bracket(participants, match_results=match_results)
	bracket.debug_print()
	return render_template('bracket.html', bracket=bracket)

@bp.route('/submit_score', methods=['POST'])
def submit_score():
	round_index = int(request.form.get("round_index"))
	match_index = int(request.form.get("match_index"))
	score1 = int(request.form.get("score1"))
	score2 = int(request.form.get("score2"))

	# Determine winner based on score input
	winner = None
	if score1 > score2:
		winner = "player1"
	elif score1 < score2:
		winner = "player2"
	else:
		# Optionally handle tie cases here
		pass

	# Save/update result in session dictionary
	match_results = session.get("match_results", {})
	key = f"r{round_index}_m{match_index}"
	match_results[key] = {"score1": score1, "score2": score2, "winner": winner}
	session["match_results"] = match_results

	return redirect(url_for("main.bracket"))