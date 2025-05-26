import pytest
from backend.models.user import User
from backend import database


def test_register_success(client):
    response = client.post("/register", json={
        "username": "новыйпользователь",
        "password": "надежныйпароль"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "новыйпользователь"
    assert "id" in data

    with client.application.app_context():
        user = User.query.filter_by(username="новыйпользователь").first()
        assert user is not None


def test_register_conflict_username(client):
    with client.application.app_context():
        user = User(username="существующий", password="хеш")
        database.session.add(user)
        database.session.commit()

    response = client.post("/register", json={
        "username": "существующий",
        "password": "любойпароль"
    })

    assert response.status_code == 409
    assert "Пользователь с таким именем уже существует" in response.get_json()["msg"]


def test_register_missing_username(client):
    response = client.post("/register", json={
        "password": "пароль123"
    })

    assert response.status_code == 422
    data = response.get_json()
    assert "username" in data.get("ошибки", {})
    assert "обязательно" in data["ошибки"]["username"][0]


def test_register_missing_password(client):
    response = client.post("/register", json={
        "username": "безпароля"
    })

    assert response.status_code == 422
    data = response.get_json()
    assert "password" in data.get("ошибки", {})
    assert "обязательно" in data["ошибки"]["password"][0]


@pytest.mark.parametrize("username,password", [
    ("", "какойтопароль"),
    ("логин", "")
])
def test_register_empty_fields(client, username, password):
    response = client.post("/register", json={
        "username": username,
        "password": password
    })

    assert response.status_code == 422
    data = response.get_json()
    if not username:
        assert "username" in data.get("ошибки", {})
    if not password:
        assert "password" in data.get("ошибки", {})