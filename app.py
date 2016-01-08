from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from flask_mail import Mail, Message
from smtplib import SMTPException
from sqlalchemy import exc
from forms import SignupForm, LoginForm
import hashlib


app = Flask(__name__)
app.config.from_pyfile('happybot.cfg')
Bootstrap(app)
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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


def create_hash(email, secret):
    return hashlib.md5(email + secret).hexdigest()


def hash_password(password, salt):
    return hashlib.sha256(password + salt).hexdigest()


@app.route('/', methods=['GET', 'POST'])
def serve_index():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.user_email.data
        code = create_hash(email, app.secret_key)
        User.query.filter_by(user_email=email).delete()
        user = User(form.user_name.data, email, form.sender_name.data, code)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            flash("Administrator of this site has not configured the database.", "error")
            return render_template('index.html', form=form)
        msg = Message("HappyBot subscription confirmation", recipients=[email])
        msg.body = "Please confirm your subscription by visiting: http://localhost:5000/confirm/" + code
        try:
            mail.send(msg)
        except SMTPException, e:
            print(e.message)
        return render_template('message.html', msg='Thank you for using HappyBot. You should receive the confirmation email soon.')

    return render_template('index.html', form=form)

@app.route('/confirm/<code>')
def serve_confirm(code):
    user = User.query.filter_by(confirmation_code=code).first()
    if user:
        user.confirmed = True
        db.session.commit()
        msg = "Subscription confirmed"
    else:
        msg = "Unknown subscription"

    return render_template('message.html', msg=msg)

@app.route('/admin')
@login_required
def serve_admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass_hash = hash_password(form.password.data, app.secret_key)
        admin = Admin.query.filter_by(password=pass_hash).first()
        if admin:
            login_user(admin)
            redirect(request.args.get('next') or url_for('admin'))
        else:
            flash("Incorrect password.", "error")
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
