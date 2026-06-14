from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

class BaseModel(DeclarativeBase): pass

PATH_DB ='sqlite:///books.db'
DB = SQLAlchemy(model_class=BaseModel)
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = PATH_DB
DB.init_app(APP)


@APP.route("/")
def index():
    return render_template('index.html')

@APP.route("/books", methods=["GET","POST"])    
def books():
    return [str(book) for book in DB.session.query(books).all()]
    if request.method == "GET": 
        return render_template('books.html')
    elif request.method == "POST":
        # Handle book creation
        pass


if __name__ == '__main__':
    APP.app_context()
    DB.create_all()      

    book1 = books(title="The Great Gatsby", author="F. Scott Fitzgerald", issn="1234567890", date_published="1925-04-10", pages=218)
    DB.session.add(book1)
    DB.session.commit()
                 
    APP.run(debug=True)                 


    