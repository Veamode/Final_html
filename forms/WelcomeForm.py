from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class WelcomeForm(FlaskForm):
    submit = SubmitField('Войти')