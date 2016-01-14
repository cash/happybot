from happybot import app, mail
import celery
from flask import url_for
from flask_mail import Message
from smtplib import SMTPException
from .text import Text


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
