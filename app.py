from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from forms import SignupForm
import hashlib


app = Flask(__name__)
app.config.from_pyfile('happybot.cfg')
Bootstrap(app)
db = SQLAlchemy(app)


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


def create_hash(email, secret):
    return hashlib.md5(email + secret).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def serve_index():
    form = SignupForm()
    if form.validate_on_submit():
        code = create_hash(form.user_email.data, app.secret_key)
        user = User(form.user_name.data, form.user_email.data, form.sender_name.data, code)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            flash("Administrator of this site has not configured the database.", "error")
            return render_template('index.html', form=form)
        # ToDo send email
        return render_template('message.html', msg='Thank you for using HappyBot. You should receive the confirmation email soon.')

    return render_template('index.html', form=form)

@app.route('/confirm')
def serve_confirm():
    return render_template('message.html', msg='Subscription confirmed')

@app.route('/admin')
def serve_admin():
    users = User.query.all()
    print users
    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run()
