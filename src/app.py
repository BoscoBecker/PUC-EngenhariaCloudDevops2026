from datetime import date

from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String
from db import DB
from Entities.book import Book

PATH_DB = 'sqlite:///books.db'
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
APP.config['SQLALCHEMY_ECHO'] = True
DB.init_app(APP)
migrate = Migrate(APP, DB)

@APP.route("/")
def index():
    return render_template('index.html')

@APP.route("/create", methods=["GET", "POST"])
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
def books():
    booksReads = DB.session.query(Book).all()
    return render_template('books.html', books=booksReads)


@APP.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = DB.session.query(Book).filter(Book.id == book_id).first()
    if book:
        DB.session.delete(book)
        DB.session.commit()
    return redirect('/books')


if __name__ == '__main__':
    with APP.app_context():
        DB.create_all()
        # try:
        #     book1 = Book(
        #         title="Fundamentos da Arquitetura de Software ",
        #         author="Mark Richards(O'Reilly)",
        #         issn="8575229680",
        #         date_published=date(2020, 1, 10),
        #         pages=432
        #     )
        #     DB.session.add(book1)
        #     DB.session.commit()
        #     print("Book inserted successfully")
        # except Exception as e:
        #     print(f"Error adding book: {e}")          


    