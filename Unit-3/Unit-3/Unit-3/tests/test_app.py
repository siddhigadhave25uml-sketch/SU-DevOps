import os
import tempfile
import pytest
from app import app
from database import init_db

@pytest.fixture()
def client(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setattr("database.DB_PATH", path)
    app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with app.test_client() as test_client:
        init_db()
        yield test_client
    os.unlink(path)

def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Library Dashboard" in response.data

def test_add_book(client):
    response = client.post("/books", data={
        "title": "Example Book", "author": "A. Writer", "isbn": "ISBN-TEST-001", "copies": "2"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Example Book" in response.data

def test_add_borrower(client):
    response = client.post("/borrowers", data={
        "name": "Test Borrower", "email": "reader@example.test"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Borrower" in response.data
