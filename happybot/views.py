from happybot import app, db, login_manager, mail
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user
from flask_mail import Message
from smtplib import SMTPException
from sqlalchemy import exc
from .forms import SignupForm, LoginForm
from .models import User, Admin
from .helpers import *
from .text import Text


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.user_email.data
        code = create_hash(email, app.secret_key)
        app.logger.info("Adding subscription for " + email)

        User.query.filter_by(user_email=email).delete()
        user = User(form.user_name.data, email, form.sender_name.data, code)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            app.logger.error("Database is not installed")
            flash(Text.error_no_db, "error")
            return render_template('index.html', form=form)
        msg = Message(Text.confirm_subject, recipients=[email])
        url = url_for('confirm', code=code, _external=True)
        msg.body = Text.confirm_body.format(url)
        try:
            mail.send(msg)
        except SMTPException, e:
            app.logger.error("Sending confirmation mail failed with '" + e.message + "'")
        return render_template('message.html', msg=Text.msg_submit)

    return render_template('index.html', form=form)

@app.route('/confirm/<code>')
def confirm(code):
    user = User.query.filter_by(confirmation_code=code).first()
    if user:
        user.confirmed = True
        db.session.commit()
        msg = Text.msg_confirmed
    else:
        msg = Text.msg_not_confirmed

    return render_template('message.html', msg=msg)

@app.route('/admin')
@login_required
def admin():
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
            flash(Text.error_password, "error")
    return render_template('login.html', form=form)
