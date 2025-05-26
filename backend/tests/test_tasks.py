def login_and_get_token(client):
    response = client.post('/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    return response.get_json()['access_token']


# === CREATE ===
def test_create_task(client):
    token = login_and_get_token(client)
    response = client.post('/tasks',
                           json={'title': 'Test Task', 'description': 'Test Description'},
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'


def test_create_task_missing_title(client):
    token = login_and_get_token(client)
    response = client.post('/tasks',
                           json={'description': 'No title'},
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 422
    assert 'errors' in response.get_json()


# === READ ===
def test_get_tasks(client):
    token = login_and_get_token(client)
    client.post('/tasks',
                json={'title': 'Task 1', 'description': 'Description 1'},
                headers={'Authorization': f'Bearer {token}'})

    response = client.get('/tasks', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.get_json()) == 1


# === UPDATE ===
def test_update_task(client):
    token = login_and_get_token(client)
    create_resp = client.post('/tasks',
                              json={'title': 'Old', 'description': ''},
                              headers={'Authorization': f'Bearer {token}'})
    task_id = create_resp.get_json()['id']

    update_resp = client.put(f'/tasks/{task_id}',
                             json={'title': 'Updated', 'is_completed': True},
                             headers={'Authorization': f'Bearer {token}'})
    assert update_resp.status_code == 200
    assert update_resp.get_json()['title'] == 'Updated'
    assert update_resp.get_json()['is_completed'] is True


def test_update_task_not_found(client):
    token = login_and_get_token(client)
    response = client.put('/tasks/999',
                          json={'title': 'Does not exist'},
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json()['msg'] == 'Task not found'


# === DELETE ===
def test_delete_task(client):
    token = login_and_get_token(client)
    create_resp = client.post('/tasks',
                              json={'title': 'To Delete', 'description': ''},
                              headers={'Authorization': f'Bearer {token}'})
    task_id = create_resp.get_json()['id']

    delete_resp = client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()['msg'] == 'Task deleted'


def test_delete_task_not_found(client):
    token = login_and_get_token(client)
    response = client.delete('/tasks/999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json()['msg'] == 'Task not found'


# === UNAUTHORIZED ===
def test_create_task_unauthorized(client):
    response = client.post('/tasks', json={'title': 'No Auth'})
    assert response.status_code == 401
    assert 'msg' in response.get_json()


def test_get_tasks_unauthorized(client):
    response = client.get('/tasks')
    assert response.status_code == 401
    assert 'msg' in response.get_json()


def test_update_task_unauthorized(client):
    response = client.put('/tasks/1', json={'title': 'New Title'})
    assert response.status_code == 401


def test_delete_task_unauthorized(client):
    response = client.delete('/tasks/1')
    assert response.status_code == 401