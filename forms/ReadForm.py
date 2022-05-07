from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class ReadForm(FlaskForm):
    prev_books = HiddenField("Ранее скачанные книги:")
    name = SelectField('Название', validators=[DataRequired()])
    submit = SubmitField('Скачать')

    def get_list(self, res):
        self.name.choices = res

    def find_prev_books(self, string):
        self.prev_books.label = "Ранее скачанные книги: \n" + string
