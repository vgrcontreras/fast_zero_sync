from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_put_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_put_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'victor contreras',
            'email': 'test@test.com',
            'password': 'batatinhas',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


# def test_get_user_n(client):
#     response = client.get('/users/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'id': 1,
#         'username': 'victor contreras',
#         'email': 'test@test.com',
#     }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
