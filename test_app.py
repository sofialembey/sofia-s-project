
from fastapi.testclient import TestClient

from app_final import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_books_returns_six_classics():
    response = client.get("/books")

    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 6
    assert len(data["books"]) == 6
    assert data["books"][0]["title"] == "Война и мир"


def test_get_book_by_id():
    response = client.get("/books/2")

    assert response.status_code == 200
    assert response.json()["title"] == "Преступление и наказание"


def test_missing_book_returns_404():
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Произведение не найдено"


def test_search_books_by_author():
    response = client.get("/books/search/Толстой")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Война и мир"
def test_search_books_by_partial_author():
    response = client.get("/books/search/Толст")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["author"] == "Лев Толстой"


def test_search_books_by_unknown_author():
    response = client.get("/books/search/НеизвестныйАвтор")

    assert response.status_code == 200
    assert response.json() == []

def test_version_returns_app_and_version():
    response = client.get("/version")

    assert response.status_code == 200

    data = response.json()
    assert data["app"] == "Каталог русской классики"
    assert data["version"] == "1.0.0"


def test_root_returns_welcome_message():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
