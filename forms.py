from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import DataRequired, Email


class SignupForm(Form):
    user_name = StringField('Your first name', validators=[DataRequired()])
    user_email = StringField('Your email address', validators=[Email()])
    sender_name = StringField("Sender's name", validators=[DataRequired()])
    submit = SubmitField('Signup')
