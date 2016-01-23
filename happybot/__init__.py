from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import os
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery
from celery.schedules import crontab


app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'happybot.cfg'))
Bootstrap(app)
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 1 * 1024 * 1024, 5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.getLevelName(app.config['LOG_LEVEL']))

jobs = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
jobs.conf.update(app.config)
jobs.conf.update({
    'CELERYBEAT_SCHEDULE': {
        'once_a_day': {
            'task': 'happybot.tasks.schedule_messages',
            'schedule': crontab(hour=0, minute=0)
        },
        'sender': {
            'task': 'happybot.tasks.send_messages',
            'schedule': crontab(minute='*/5')
        }
    }
})

from happybot import views
