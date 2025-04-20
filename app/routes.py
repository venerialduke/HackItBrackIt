from flask import Blueprint, render_template, request, redirect, url_for
from .models import Participant
from . import db

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

def generate_avatar_filename(name, color, show):
	index = (hash(name + color + show) % 8) + 1
	return f'avatar{index}.png'

@bp.route('/bracket', methods=['GET', 'POST'])
def bracket():
	from .models import Participant
	participants = Participant.query.all()

	# Handle form submission
	if request.method == 'POST':
		print("Form submitted:", request.form)

		# Optional: Parse submitted scores
		try:
			# Example: grabbing score inputs based on player IDs
			player1_id = int(request.form.get('player1_id'))
			player2_id = int(request.form.get('player2_id'))
			score1 = int(request.form.get(f'score_{player1_id}'))
			score2 = int(request.form.get(f'score_{player2_id}'))

			print(f"Game result: {player1_id} ({score1}) vs {player2_id} ({score2})")

			# TODO: store result, advance winner, etc.
		except Exception as e:
			print("Error parsing form:", e)

		# Redirect to GET version to prevent form resubmission
		return redirect(url_for('main.bracket'))

	# TEMPORARY hardcoded matchups (we’ll improve this soon)
	matchups = []
	if len(participants) >= 2:
		matchups.append((participants[0], participants[1]))
	if len(participants) >= 4:
		matchups.append((participants[2], participants[3]))

	return render_template('bracket.html', matchups=matchups)