from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = FileField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Добавить')