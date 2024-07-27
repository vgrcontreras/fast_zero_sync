from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act  (ação)

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Olá Mundo!'}  # assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'victor',
            'password': 'batatinhas',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'victor',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'victor', 'email': 'test@test.com', 'id': 1}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'victor contreras',
            'email': 'test@test.com',
            'password': 'batatinhas',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'victor contreras',
        'email': 'test@test.com',

    }


def test_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'victor contreras',
            'email': 'test@test.com',
            'password': 'batatinhas',
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
