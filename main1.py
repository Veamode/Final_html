import os
import uuid

from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_login import login_user, login_required, logout_user
from flask_restful import Api

from data.book_user import Book_User
from tests import user_api
# from tests import right_api
# from tests import book_api
from forms.AddForm import AddForm
from forms.LoginForm import LoginForm
from forms.ReadForm import ReadForm
from forms.RegisterForm import RegisterForm
from data import db_session
from data.books import Book
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eb5aa595-0377-4303-8464-942707623c6f'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = '/storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if not db_sess.query(Book).filter(Book.name == form.title.data).first():
            book = Book()
            book.name = form.title.data
            file = form.content.data
            s = str(file.content_type).split('/')
            if s[1] not in ALLOWED_EXTENSIONS:
                return render_template('book_add.html',
                                       title='Добавление книги',
                                       message='Неподдерживаемый формат',
                                       form=form)
            book.context = str(uuid.uuid4()) + '.' + str(file.filename).split('.')[-1]
            Image.open(file)
            file.save('storage/{}'.format(book.context))
            db_sess.add(book)
            db_sess.commit()
            return render_template('book_add.html',
                                   title='Добавление книги',
                                   message='Книга успешно добавлена',
                                   form=form)
        return render_template('book_add.html',
                               title='Добавление книги',
                               message='Книга с таким названием уже существует',
                               form=form)
    return render_template('book_add.html',
                           title='Добавление книги',
                           form=form)


@app.route('/choose_book', methods=['GET', 'POST'])
def choose_book():
    if current_user.is_authenticated:
        if current_user.right_id == 1:
            return redirect('/add_book')
    form = ReadForm()
    db_sess = db_session.create_session()
    result = db_sess.query(Book.name).all()
    result = list(map(lambda x: x[0], result))
    form.get_list(result)
    find_book = db_sess.query(Book_User.book_id).filter(Book_User.user_id == current_user.id).all()
    find_book_id = list(map(lambda x: x[0], find_book))
    find_book_name = ''

    for i in find_book_id:
        find_book_name += str(list(map(lambda x: x[0],
                                       db_sess.query(Book.name).
                                       filter(Book.id == i).all()))[0]) + ';    '
    form.find_prev_books(find_book_name)
    if form.validate_on_submit():
        result = db_sess.query(Book.context).filter(Book.name == form.name.data).first()
        homeDir = os.path.expanduser("~")
        try:
            file = open('storage/{}'.format(result[0]), "rb")
            f = open('{}/{}'.format(homeDir, result[0]), "wb")
            f.write(file.read())
            f.close()
        except FileNotFoundError:
            return render_template('book_read.html',
                                   title='Скачать книгу',
                                   message='Книга "{}" не была скачана, возникла ошибка'.
                                   format(form.name.data),
                                   form=form)
        add_load_book = db_sess.query(Book.id).filter(Book.name == form.name.data).first()[0]
        result1 = db_sess.query(Book_User.id).filter(Book_User.book_id == add_load_book).filter(
                                                     Book_User.user_id == current_user.id).first()

        if not result1:
            new_book = Book_User(user_id=current_user.id,
                                 book_id=add_load_book)
            db_sess.add(new_book)
            db_sess.commit()
        return render_template('book_read.html',
                               title='Скачать книгу',
                               message='Книга "{}" успешно скачана в папку "{}" с названием "{}"'.
                               format(form.name.data, homeDir, result[0]),
                               form=form)
    return render_template('book_read.html', title='Скачать книгу',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.right_id == 1:
            return redirect('/add_book')
        else:
            return redirect('/choose_book')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.right_id == 1:
                return redirect("/add_book")
            else:
                return redirect("/choose_book")
        return render_template('login1.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login1.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    # app.register_blueprint(book_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    # app.register_blueprint(right_api.blueprint)
    app.run()
