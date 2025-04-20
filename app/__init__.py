from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'your_secret_key'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)

	with app.app_context():
		from . import routes  # <- this loads bp from routes.py
		app.register_blueprint(routes.bp)  # <- this registers all routes
		from . import models
		db.create_all()

	return app