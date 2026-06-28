from datetime import date

from flask import Flask, app, render_template, request, redirect, send_from_directory
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate

from sqlalchemy import text
from Entities.users import User
from Entities.book import Book

from db import DB
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

PATH_DB = 'sqlite:///books.db'
APP = Flask(__name__)
APP.secret_key = secrets.token_hex(32)
APP.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
APP.config['SQLALCHEMY_ECHO'] = True
DB.init_app(APP)
migrate = Migrate(APP, DB)

login_manager = LoginManager()
login_manager.init_app(APP)

login_manager.login_view = '/login' 
login_manager.login_message = "Por favor, faça login para acessar esta página."

@login_manager.user_loader
def load_user(user_id):
    return DB.session.get(User, int(user_id))

@APP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = DB.session.query(User).filter(User.username == username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")

@APP.route("/")
@login_required
def index():
    return render_template('index.html')

@APP.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template('create.html')

    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        issn = request.form['issn']
        date_published_str = request.form['date_published']
        pages = request.form['pages']

        # Convert string date to date object
        date_published = date.fromisoformat(date_published_str)

        book = Book(
            title=title,
            author=author,
            issn=issn,
            date_published=date_published,
            pages=pages
        )
        DB.session.add(book)
        DB.session.commit()
        return redirect('/books')

@APP.route("/books", methods=["GET"])
@login_required
def books():
    booksReads = DB.session.query(Book).all()
    return render_template('books.html', books=booksReads)

@APP.route("/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):
    book = DB.session.query(Book).filter(Book.id == book_id).first()
    if book:
        DB.session.delete(book)
        DB.session.commit()
    return redirect('/books')

@APP.route("/createuser", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template('create_user.html')

    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            date_joined=date.today()
        )
        DB.session.add(user)
        DB.session.commit()
        return redirect('/login')

@APP.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@APP.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    with APP.app_context():
        DB.create_all()
