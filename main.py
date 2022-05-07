import os
import pathlib
import shutil
import sqlite3
import uuid

from flask import Flask, render_template, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user
from flask_login import login_required, logout_user
from flask_restful import Api

# from data.book_user import Book_User
from werkzeug.utils import secure_filename

from forms.Downloaded import DownForm
from forms.WelcomeForm import WelcomeForm
from tests import user_api
# from tests import right_api
# from tests import book_api
from forms.AddForm import AddForm
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from data import db_session, users
from data.books import Book
from data.users import User
from forms.MainForm import MainForm
from PIL import Image

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


# @app.route('/choose_book', methods=['GET', 'POST'])
# def choose_book():
#     if current_user.is_authenticated:
#         if current_user.right_id == 1:
#             return redirect('/add_book')
#     form = ReadForm()
#     db_sess = db_session.create_session()
#     result = db_sess.query(Book.name).all()
#     result = list(map(lambda x: x[0], result))
#     form.get_list(result)
#     find_book = db_sess.query(Book_User.book_id).filter(Book_User.user_id == current_user.id).all()
#     find_book_id = list(map(lambda x: x[0], find_book))
#     find_book_name = ''
#
#     for i in find_book_id:
#         find_book_name += str(list(map(lambda x: x[0],
#                                        db_sess.query(Book.name).
#                                        filter(Book.id == i).all()))[0]) + ';    '
#     form.find_prev_books(find_book_name)
#     if form.validate_on_submit():
#         result = db_sess.query(Book.context).filter(Book.name == form.name.data).first()
#         homeDir = os.path.expanduser("~")
#         try:
#             file = open('storage/{}'.format(result[0]), "rb")
#             f = open('{}/{}'.format(homeDir, result[0]), "wb")
#             f.write(file.read())
#             f.close()
#         except FileNotFoundError:
#             return render_template('book_read.html',
#                                    title='Скачать книгу',
#                                    message='Книга "{}" не была скачана, возникла ошибка'.
#                                    format(form.name.data),
#                                    form=form)
#         add_load_book = db_sess.query(Book.id).filter(Book.name == form.name.data).first()[0]
#         result1 = db_sess.query(Book_User.id).filter(Book_User.book_id == add_load_book).filter(
#                                                      Book_User.user_id == current_user.id).first()
#
#         if not result1:
#             new_book = Book_User(user_id=current_user.id,
#                                  book_id=add_load_book)
#             db_sess.add(new_book)
#             db_sess.commit()
#         return render_template('book_read.html',
#                                title='Скачать книгу',
#                                message='Книга "{}" успешно скачана в папку "{}" с названием "{}"'.
#                                format(form.name.data, homeDir, result[0]),
#                                form=form)
#     return render_template('book_read.html', title='Скачать книгу',
#                            form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/', methods=['GET', 'POST'])
def mission():
    form = WelcomeForm()
    return render_template('welcome.html', form=form)


@app.route('/main', methods=['GET', 'POST'])
def not_so_main():
    form = MainForm()
    print(current_user.is_authenticated)
    if form.submit():
        pass
        # if not form.search.text:
        #     print(12121313)
        # db_sess = db_session.create_session()

    return render_template('main_form.html', form=form)


@app.route('/main/add_photo', methods=['GET', 'POST'])
def add_photo():
    print(121212121212)
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()

        if not db_sess.query(Book).filter(Book.name == form.title.data).first():
            book = Book()
            book.name = form.title.data
            # book.person_id = db_sess.query(User).filter(users.id)

            book.person_id = 1
            file = form.content.data
            s = str(file.content_type).split('/')
            if s[1] not in ALLOWED_EXTENSIONS:
                return render_template('book_add.html',
                                       title='Добавление книги',
                                       message='Неподдерживаемый формат',
                                       form=form)
            # book.context = str(uuid.uuid4()) + '.' + str(file.filename).split('.')[-1]
            book.context = form.title.data + '.' + s[1]

            file.save('static/photos_xrenotos/{}'.format(book.context))

            print(1111111111)
            db_sess.add(book)
            db_sess.commit()
            return render_template('add_photo.html',
                                   message="Зашибись",
                                   form=form)
    return render_template('add_photo.html', form=form)


@app.route('/main/downloaded', methods=['GET', 'POST'])
def urs_photo():
    form = DownForm()
    # form.title.data = open('last_down.txt').read()
    # pict = Image.open(form.title.data)
    # form.content.data = pict
    return render_template('downloaded.html', form=form)


@app.route('/main/download', methods=['GET', 'POST'])
def down(search):
    results = []
    search_string = search.data['search']
    print(search_string)

    if search.data['search'] == '':
        qry = db_session.query('database.db')
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/main')
    else:
        # display results
        return render_template('results.html', results=results)
    return redirect('/main')


# @app.route('/main/download', methods=['GET', 'POST'])
# def down(search):
#     results = []
#     search_string = search.data['search']
#     print(search_string)
#
#     if search.data['search'] == '':
#         qry = db_session.query('database.db')
#         results = qry.all()
#
#     if not results:
#         flash('No results found!')
#         return redirect('/main')
#     else:
#         # display results
#         return render_template('results.html', results=results)
#     return redirect('/main')


@app.route('/main/download1', methods=['GET', 'POST'])
def down_one():
    # shutil.copy('D:/Pycharm/Project_of_html/static/photos_xrenotos/1.jpg',
    #             "D:/Pycharm/Project_of_html/static/photos_down/1.jpg")
    # conn = sqlite3.connect('db/database.db')
    # cursor = conn.cursor()
    # cursor.execute('INSERT INTO photos VALUES(1.jpg, shrek, {})'.format(current_user.id))
    l_down = '1.jpg'
    f = open('db/last_down.txt', 'w')
    f.write(l_down)
    f.close()
    return redirect('/main')


@app.route('/main/download2', methods=['GET', 'POST'])
def down_two():
    # shutil.copy('D:/Pycharm/Project_of_html/static/photos_xrenotos/2.png',
    #             "D:/Pycharm/Project_of_html/static/photos_down/2.png")
    l_down = '2.png'
    f = open('db/last_down.txt', 'w')
    f.write(l_down)
    f.close()
    return redirect('/main')


@app.route('/main/download3', methods=['GET', 'POST'])
def down_three():
    # shutil.copy('D:/Pycharm/Project_of_html/static/photos_xrenotos/3.jpg',
    #             "D:/Pycharm/Project_of_html/static/photos_down/3.jpg")
    l_down = '3.png'
    f = open('db/last_down.txt', 'w')
    f.write(l_down)
    f.close()
    return redirect('/main')


@app.route('/main/download4', methods=['GET', 'POST'])
def down_four():
    # shutil.copy('D:/Pycharm/Project_of_html/static/photos_xrenotos/4.jpg',
    #             "D:/Pycharm/Project_of_html/static/photos_down/4.jpg")
    l_down = '4.png'
    f = open('db/last_down.txt', 'w')
    f.write(l_down)
    f.close()
    return redirect('/main')


@app.route('/main/download5', methods=['GET', 'POST'])
def down_five():
    # shutil.copy('D:/Pycharm/Project_of_html/static/photos_xrenotos/5.jpg',
    #             "D:/Pycharm/Project_of_html/static/photos_down/5.jpg")
    l_down = '5.png'
    f = open('db/last_down.txt', 'w')
    f.write(l_down)
    f.close()
    return redirect('/main')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.right_id == 1:
            return redirect('/add_book')
        else:
            return redirect('/main')
    form = LoginForm()
    if form.validate_on_submit():
        print(1)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.right_id == 1:
                return redirect("/add_book")
            else:
                return redirect("/main")
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
    app.run(port=5550, host='127.0.0.1')
