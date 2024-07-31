from fast_zero.models import User


def test_create_user(session):
    user = User(username='user', password='senha', email='test2@test.com')

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id == 1
