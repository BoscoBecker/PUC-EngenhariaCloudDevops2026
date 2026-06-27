import pytest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import APP, DB
from Entities.book import Book

@pytest.fixture()
def app():
    APP.config.update({"TESTING": True})
    return APP

@pytest.fixture()
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert "" !=  response.data


def test_books_page_has_create_button(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert b"Cadastrar livro" in response.data
    assert b'href="/create"' in response.data


def test_create_page_renders(client):
    response = client.get("/create")
    assert response.status_code == 200
    assert b"Cadastrar livro" in response.data
    assert b'action="/create"' in response.data
    assert b'method="post"' in response.data


def test_create_book_redirects_to_books(client):
    response = client.post("/create", data={
        "title": "Test Book",
        "author": "Test Author",
        "issn": "1234567890",
        "date_published": "2024-01-01",
        "pages": "100"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.location == "/books"


def test_books_page_has_delete_button(client):
    # Create a book first
    client.post("/create", data={
        "title": "Test Book",
        "author": "Test Author",
        "issn": "1234567890",
        "date_published": "2024-01-01",
        "pages": "100"
    }, follow_redirects=True)

    # Check that delete button exists
    response = client.get("/books")
    assert response.status_code == 200
    assert b"Deletar" in response.data
    assert b'/delete/' in response.data


def test_delete_book_redirects_to_books(app, client):
    # Create a book first
    client.post("/create", data={
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
    response = client.post(f"/delete/{book_id}", follow_redirects=False)
    assert response.status_code == 302
    assert response.location == "/books"

    # Verify the book was deleted
    with app.app_context():
        deleted_book = DB.session.query(Book).filter(Book.id == book_id).first()
        assert deleted_book is None
    