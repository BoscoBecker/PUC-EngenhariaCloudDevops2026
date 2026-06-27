import pytest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import APP

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
    