# -*- coding: utf-8 -*-

# Email bodies are in the template directory

class Text(object):
    msg_submit = 'Thank you for using HappyBot. You should receive the confirmation email soon.'
    msg_confirmed = 'Subscription confirmed.'
    msg_not_confirmed = 'Unknown subscription.'
    msg_unsubscribed = 'You have been unsubscribed.'

    confirm_subject = 'HappyBot confirmation'
    message_subject = 'Hey {0}'

    error_no_db = 'Administrator of this site has not configured the database.'
    error_password = 'Incorrect password.'
