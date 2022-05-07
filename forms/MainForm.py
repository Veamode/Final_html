from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, FileField, SelectField, StringField, SearchField
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    content = FileField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Поиск')
    select = SelectField()
    search = SearchField('')