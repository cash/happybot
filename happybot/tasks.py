from happybot import app, mail, db
import celery
from flask import url_for
from flask_mail import Message
from smtplib import SMTPException
import datetime
from .text import Text
from .models import User, MessageSchedule
from .helpers import *


@celery.task
def send_confirm_email(user_data):
    with app.app_context():
        msg = Message(Text.confirm_subject, recipients=[user_data['user_email']])
        confirm_url = url_for('confirm', code=user_data['confirmation_code'], _external=True)
        home_url = url_for('index', _external=True)
        msg.html = Text.confirm_body.format(user_data['sender_name'], confirm_url, home_url)
        try:
            mail.send(msg)
        except SMTPException, e:
            app.logger.error("Sending confirmation mail failed with '" + e.message + "'")

@celery.task
def schedule_messages():
    app.logger.info("Scheduling messages")
    MessageSchedule.query.delete()
    for user in User.query.all():
        time = create_schedule_time(app.config['HAPPYBOT_START'], app.config['HAPPYBOT_STOP'])
        app.logger.warn(time)
        entry = MessageSchedule(user.id, time)
        db.session.add(entry)
    db.session.commit()

@celery.task
def send_messages():
    for entry in MessageSchedule.query.filter(MessageSchedule.msg_time < datetime.datetime.now().time()).all():
        user = User.query.filter_by(id=entry.user_id).first()
        msg = Message(Text.confirm_subject, recipients=[user.user_email])
        unsub_url = url_for('unsubscribe', code=user.confirmation_code, _external=True)
        home_url = url_for('index', _external=True)
        msg.html = Text.confirm_body.format(user.sender_name, unsub_url, home_url)
        db.session.delete(entry)
    db.session.commit()
