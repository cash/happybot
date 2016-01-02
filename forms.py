from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import DataRequired, Email


class SignupForm(Form):
    user_name = TextField('Your first name', validators=[DataRequired()])
    user_email = TextField('Your email address', validators=[Email()])
    sender_name = TextField("Sender's name", validators=[DataRequired()])
    submit = SubmitField('Signup')
