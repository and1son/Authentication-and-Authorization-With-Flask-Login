from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'thisismysecretkey'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

	db.init_app(app)

	login_manager = LoginManager() #ako nije logiran da ga vrati na login
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	#u cookie se sprema id korisnika, flask login trazi login id u cookiju i tako ga pronade u bazi
	#UserMixin sluzi za to

	from .models import User

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id)) #asocira id u cookieju sa id-jem objekta

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

