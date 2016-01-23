from happybot import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80))
    user_email = db.Column(db.String(120), index=True, unique=True)
    sender_name = db.Column(db.String(80))
    confirmation_code = db.Column(db.String(32))
    confirmed = db.Column(db.Boolean)

    def __init__(self, user_name, email, sender_name, code):
        self.user_name = user_name
        self.user_email = email
        self.sender_name = sender_name
        self.confirmation_code = code
        self.confirmed = False

    def __repr__(self):
        return "<User {0} with email {1}>".format(self.user_name, self.user_email)

    def get_dict(self):
        # this is to support passing the data to async tasks
        return {
            'user_name': self.user_name,
            'user_email': self.user_email,
            'sender_name': self.sender_name,
            'confirmation_code': self.confirmation_code,
            'confirmed': self.confirmed
        }


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))

    def __init__(self, password):
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class MessageSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    msg_time = db.Column(db.Time, index=True)

    def __init__(self, user_id, scheduled_time):
        self.user_id = user_id
        self.msg_time = scheduled_time
