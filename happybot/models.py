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
