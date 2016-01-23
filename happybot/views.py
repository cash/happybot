from happybot import app, db, login_manager
from flask import render_template, flash, redirect, request
from flask_login import login_required, login_user
from sqlalchemy import exc
from .forms import SignupForm, LoginForm
from .models import Subscription, Admin
from .helpers import *
from .text import Text
from .tasks import *


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.user_email.data
        code = create_hash(email, app.secret_key)
        app.logger.info("Adding subscription for " + email)

        Subscription.query.filter_by(user_email=email).delete()
        user = Subscription(form.user_name.data, email, form.sender_name.data, code)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            app.logger.error("Database is not installed")
            flash(Text.error_no_db, "error")
            return render_template('index.html', form=form)
        send_confirm_email.delay(user.get_dict())
        return render_template('status.html', msg=Text.msg_submit)

    return render_template('index.html', form=form)

@app.route('/confirm/<code>')
def confirm(code):
    app.logger.info("Confirming subscription with code " + code)
    user = Subscription.query.filter_by(confirmation_code=code).first()
    if user:
        user.confirmed = True
        db.session.commit()
        msg = Text.msg_confirmed
    else:
        msg = Text.msg_not_confirmed

    return render_template('status.html', msg=msg)

@app.route('/unsubscribe/<code>')
def unsubscribe(code):
    app.logger.info("Unsubscribing user with code " + code)
    Subscription.query.filter_by(confirmation_code=code).delete()
    db.session.commit()
    return render_template('status.html', msg=Text.msg_unsubscribed)

@app.route('/admin')
@login_required
def admin():
    users = Subscription.query.all()
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
