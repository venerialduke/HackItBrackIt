from flask import render_template, request, redirect, url_for
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

def generate_avatar_filename(name, color, show):
	index = (hash(name + color + show) % 8) + 1
	return f'avatar{index}.png'

@bp.route('/bracket', methods=['GET', 'POST'])
def bracket():
	from .bracket_logic import Bracket
	participants = Participant.query.all()
	bracket = Bracket(participants)

	# Debug output
	bracket.debug_print()

	return render_template('bracket.html', bracket=bracket)