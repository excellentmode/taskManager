import pytest


def test_login_success(client):
    response = client.post('/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()


def test_login_failure_wrong_password(client):
    response = client.post('/login', json={
        'username': 'admin',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == '401 Unauthorized: Invalid credentials'


def test_login_failure_missing_fields(client):
    response = client.post('/login', json={
        'username': 'admin'
    })
    assert response.status_code == 422
    data = response.get_json()
    assert 'Ошибки' in data
    assert 'password' in data['Ошибки']


@pytest.mark.parametrize(
    "username,password",
    [
        ("", "admin123"),
        ("admin", ""),
        ("", ""),
    ])
def test_login_empty_fields(client, username, password):
    response = client.post('/login', json={
        'username': username,
        'password': password
    })
    assert response.status_code == 422
    data = response.get_json()
    assert 'Ошибки' in data
    if username == "":
        assert 'username' in data['Ошибки']
    if password == "":
        assert 'password' in data['Ошибки']