from happybot import app, mail, db
import celery
from flask import url_for, render_template
from flask_mail import Message
from smtplib import SMTPException
import datetime
from .text import Text
from .models import Subscription, MessageSchedule
from .helpers import *


@celery.task
def send_confirm_email(user_data):
    with app.app_context():
        app.logger.info("Sending confirmation to " + user_data['user_email'])
        msg = Message(Text.confirm_subject, recipients=[user_data['user_email']])
        confirm_url = url_for('confirm', code=user_data['confirmation_code'], _external=True)
        home_url = url_for('index', _external=True)
        msg.html = render_template('confirm_email.html', sender_name=user_data['sender_name'], confirm_url=confirm_url,
                                   home_url=home_url)
        msg.body = render_template('confirm_email.txt', sender_name=user_data['sender_name'], confirm_url=confirm_url,
                                   home_url=home_url)
        try:
            mail.send(msg)
        except SMTPException, e:
            app.logger.error("Sending confirmation mail failed with '" + e.message + "'")

@celery.task
def schedule_happy_messages():
    with app.app_context():
        app.logger.info("Scheduling happy messages")
        count = 0
        MessageSchedule.query.delete()
        for subscription in Subscription.query.all():
            time = create_schedule_time(app.config['HAPPYBOT_START'], app.config['HAPPYBOT_STOP'])
            entry = MessageSchedule(subscription.id, time)
            db.session.add(entry)
            count += 1
        db.session.commit()
        app.logger.info("Number of scheduled messages: {0}".format(count))

@celery.task
def send_happy_messages():
    with app.app_context():
        app.logger.info("Sending happy messages")
        count = 0
        personality = Personality('happybot', 'happybot/personalities/happybot.txt')
        for entry in MessageSchedule.query.filter(MessageSchedule.msg_time < datetime.datetime.now().time()).all():
            subscription = Subscription.query.filter_by(id=entry.user_id).first()
            subject = Text.message_subject.format(subscription.user_name)
            msg = Message(subject, recipients=[subscription.user_email])
            unsub_url = url_for('unsubscribe', code=subscription.confirmation_code, _external=True)
            home_url = url_for('index', _external=True)
            message = personality.get_message()
            msg.html = render_template('happy_message.html', user_name=subscription.user_name, message=message,
                                       sender_name=subscription.sender_name, home_url=home_url,
                                       unsubscribe_url=unsub_url)
            msg.body = render_template('happy_message.txt', user_name=subscription.user_name, message=message,
                                        sender_name=subscription.sender_name, home_url=home_url,
                                        unsubscribe_url=unsub_url)

            try:
                mail.send(msg)
                count += 1
            except SMTPException, e:
                app.logger.error("Sending happy message failed with '" + e.message + "'")
            db.session.delete(entry)
        db.session.commit()
        app.logger.info("Number of messages sent: {0}".format(count))
