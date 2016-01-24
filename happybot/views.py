from happybot import app, db, login_manager
from flask import render_template, flash, redirect, request
from flask_login import login_required, login_user, logout_user
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
        subscription = Subscription(form.user_name.data, email, form.sender_name.data, code)
        db.session.add(subscription)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            app.logger.error("Database is not installed")
            flash(Text.error_no_db, "error")
            return render_template('index.html', form=form)
        send_confirm_email.delay(subscription.get_dict())
        return render_template('status.html', msg=Text.msg_submit)

    return render_template('index.html', form=form)

@app.route('/confirm/<code>')
def confirm(code):
    app.logger.info("Confirming subscription with code " + code)
    subscription = Subscription.query.filter_by(confirmation_code=code).first()
    if subscription:
        subscription.confirmed = True
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
@app.route('/admin/subs')
@app.route('/admin/subs/<int:page>')
@login_required
def admin_subs(page=1):
    subscriptions = Subscription.query.order_by(db.desc(Subscription.id)).paginate(page, 25, False)
    return render_template('subscriptions.html', subscriptions=subscriptions)

@app.route('/admin/schedule')
@app.route('/admin/schedule/<int:page>')
@login_required
def admin_schedule(page=1):
    schedule = MessageSchedule.query.paginate(page, 25, False)
    return render_template('schedule.html', schedule=schedule)

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
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(Text.error_password, "error")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))