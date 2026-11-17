from app.models.user import User


def register_user(client, username="astronaut_test",
                  email="astronaut@test.com", password="Password123"):
    return client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": password
        },
        follow_redirects=False
    )


def test_register_page_loads(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_user_successfully(client, app):
    response = register_user(client)

    assert response.status_code == 302

    with app.app_context():
        user = User.query.filter_by(username="astronaut_test").first()
        assert user is not None
        assert user.email == "astronaut@test.com"
        assert user.role == "astronaut"
        assert user.check_password("Password123")


def test_register_rejects_empty_fields(client):
    response = client.post(
        "/auth/register",
        data={"username": "", "email": "", "password": ""}
    )

    assert response.status_code == 302


def test_register_rejects_short_password(client):
    response = register_user(client, password="123")

    assert response.status_code == 302


def test_register_rejects_duplicate_username(client):
    register_user(client)

    response = register_user(
        client,
        username="astronaut_test",
        email="another@test.com"
    )

    assert response.status_code == 302


def test_register_rejects_duplicate_email(client):
    register_user(client)

    response = register_user(
        client,
        username="another_user",
        email="astronaut@test.com"
    )

    assert response.status_code == 302


def test_login_with_valid_credentials(client):
    register_user(client)

    response = client.post(
        "/auth/login",
        data={
            "email": "astronaut@test.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "_user_id" in session


def test_login_rejects_invalid_password(client):
    register_user(client)

    response = client.post(
        "/auth/login",
        data={
            "email": "astronaut@test.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "unknown@test.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 200


def test_logout_requires_authentication(client):
    response = client.get("/auth/logout")

    assert response.status_code == 302


def test_logout_authenticated_user(client):
    register_user(client)

    client.post(
        "/auth/login",
        data={
            "email": "astronaut@test.com",
            "password": "Password123"
        }
    )

    response = client.get("/auth/logout")

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "_user_id" not in session
