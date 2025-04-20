print("models.py loaded")
from . import db

class Participant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	favorite_color = db.Column(db.String(50))
	favorite_show = db.Column(db.String(100))
	avatar_filename = db.Column(db.String(100))  # path to avatar image