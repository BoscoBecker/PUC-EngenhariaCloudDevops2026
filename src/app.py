from datetime import date

from flask import Flask, render_template, request
from sqlalchemy import DateTime, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy


class BaseModel(DeclarativeBase): pass

PATH_DB ='sqlite:///books.db'
DB = SQLAlchemy(model_class=BaseModel)
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
APP.config['SQLALCHEMY_ECHO'] = True
DB.init_app(APP)


@APP.route("/")
def index():
    return render_template('index.html')

@APP.route("/books", methods=["GET","POST"])    
def books():    
    if request.method == "GET": 
        booksReads = DB.session.query(books).all()
        return render_template('books.html', books=booksReads)
    elif request.method == "POST":
        # Handle book creation
        pass


if __name__ == '__main__':
    with APP.app_context():
        DB.create_all()
        
        from Entities.book import Book
        print("Database created successfully.")
        DB.session.execute(text("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(256) NOT NULL,
                author VARCHAR(256) NOT NULL,
                issn VARCHAR(16) NOT NULL,
                date_published DATETIME NOT NULL,
                pages INTEGER NOT NULL
                )"""))
        DB.session.commit()
        # try:
        #     book1 = Book(
        #         title="The Great Gatsby",
        #         author="F. Scott Fitzgerald",
        #         issn="1234567890",
        #         date_published=date(1925, 4, 10),
        #         pages=218
        #     )
        #     DB.session.add(book1)
        #     DB.session.commit()
        #     print("Book inserted successfully")
        # except Exception as e:
        #     print(f"Error adding book: {e}")          


    