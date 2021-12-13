from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from configs import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
# make the application an instance from SQLAlchamy
db = SQLAlchemy(app)
# define db migration
migrate = Migrate(app, db)
# provide hash utilities for app
bcrypt = Bcrypt(app)
# set up a login manager for app
login_manager = LoginManager(app)
# set the login route when the app tries to access login_required
login_manager.login_view = 'main.index'
# set a category info to give the login message style
login_manager.login_message_category = 'info'

# call all the routes to run after initializing db and app
from flaskr.main.routes import main


app.register_blueprint(main)
