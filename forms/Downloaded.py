from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class DownForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    # content = FileField("Содержание", validators=[DataRequired()])
    content = FileField(default='1.jpg', )