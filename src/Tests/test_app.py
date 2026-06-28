import pytest
import sys
import os
from werkzeug.security import generate_password_hash

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import APP, DB
from Entities.book import Book
from Entities.users import User  

@pytest.fixture
def authenticated_client(client, app):
    with app.app_context():
        user = DB.session.query(User).filter_by(username="teste").first()

        if user is None:
            user = User(
                username="teste",
                password=generate_password_hash("123456"),
                email="teste@example.com",
                date_joined=getattr(__import__('datetime'), 'date').today()
            )
            DB.session.add(user)
            DB.session.commit()

    client.post("/login", data={
        "username": "teste",
        "password": "123456"
    })

    return client

@pytest.fixture()
def app():
    APP.config.update({"TESTING": True})
    return APP

@pytest.fixture()
def client(app):
    return app.test_client()


def test_index(authenticated_client):
    response = authenticated_client.get("/books")
    assert response.status_code == 200
    assert "" !=  response.data


def test_books_page_has_create_button(authenticated_client):
    response = authenticated_client.get("/books")
    assert response.status_code == 200
    assert b"Cadastrar livro" in response.data
    assert b'href="/create"' in response.data


def test_create_page_renders(authenticated_client):
    response = authenticated_client.get("/create")
    assert response.status_code == 200
    assert b"Cadastrar livro" in response.data
    assert b'action="/create"' in response.data
    assert b'method="post"' in response.data


def test_create_book_redirects_to_books(authenticated_client):
    response = authenticated_client.post("/create", data={
        "title": "Test Book",
        "author": "Test Author",
        "issn": "1234567890",
        "date_published": "2024-01-01",
        "pages": "100"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.location == "/books"


def test_books_page_has_delete_button(authenticated_client):
    # Create a book first
    authenticated_client.post("/create", data={
        "title": "Test Book",
        "author": "Test Author",
        "issn": "1234567890",
        "date_published": "2024-01-01",
        "pages": "100"
    }, follow_redirects=True)

    # Check that delete button exists
    response = authenticated_client.get("/books")
    assert response.status_code == 200
    assert b"Deletar" in response.data
    assert b'/delete/' in response.data


def test_delete_book_redirects_to_books(app, authenticated_client):
    # Create a book first
    authenticated_client.post("/create", data={
        "title": "Test Book",
        "author": "Test Author",
        "issn": "1234567890",
        "date_published": "2024-01-01",
        "pages": "100"
    }, follow_redirects=True)

    # Get the book ID from the database within app context
    with app.app_context():
        book = DB.session.query(Book).first()
        book_id = book.id

    # Delete the book
    response = authenticated_client.post(f"/delete/{book_id}", follow_redirects=False)
    assert response.status_code == 302
    assert response.location == "/books"

    # Verify the book was deleted
    with app.app_context():
        deleted_book = DB.session.query(Book).filter(Book.id == book_id).first()
        assert deleted_book is None
    