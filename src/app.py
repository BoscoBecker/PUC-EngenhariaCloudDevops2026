from datetime import date

from flask import Flask, render_template, request
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

@APP.route("/books", methods=["GET","POST"])    
def books():    
    if request.method == "GET": 
        booksReads = booksReads = DB.session.query(Book).all()
        return render_template('books.html', books=booksReads)
    elif request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        issn = request.form['issn']
        date_published = request.form['date_published']
        pages = request.form['pages']

        book = Book(
            title=title,
            author=author,
            issn=issn,
            date_published=date_published,
            pages=pages
        )
        DB.session.add(book)
        DB.session.commit()
        return render_template('books.html', booksReads = DB.session.query(Book).all())


if __name__ == '__main__':
    with APP.app_context():
        DB.create_all()
        
        # print("Database created successfully.")
        # DB.session.execute(text("""
        #     CREATE TABLE IF NOT EXISTS books (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         title VARCHAR(256) NOT NULL,
        #         author VARCHAR(256) NOT NULL,
        #         issn VARCHAR(16) NOT NULL,
        #         date_published DATETIME NOT NULL,
        #         pages INTEGER NOT NULL
        #         )"""))
        # DB.session.commit()
        try:
            book1 = Book(
                title="Fundamentos da Arquitetura de Software ",
                author="Mark Richards(O'Reilly)",
                issn="8575229680",
                date_published=date(2020, 1, 10),
                pages=432
            )
            DB.session.add(book1)
            DB.session.commit()
            print("Book inserted successfully")
        except Exception as e:
            print(f"Error adding book: {e}")          


    