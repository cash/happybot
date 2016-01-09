from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'happybot.cfg'))
Bootstrap(app)
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from happybot import views
