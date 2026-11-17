from app.models.user import User
from app.models.alert import Alert
from app.extensions import db


def create_and_login_user(client, username="alert_user",
                          email="alert_user@test.com"):
    client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": "Password123"
        }
    )

    client.post(
        "/auth/login",
        data={
            "email": email,
            "password": "Password123"
        }
    )


def test_alerts_requires_login(client):
    response = client.get("/alerts/")
    assert response.status_code == 302


def test_create_alert(client, app):
    create_and_login_user(client)

    response = client.post(
        "/alerts/create",
        data={
            "title": "Alerta de prueba",
            "message": "Verificación automatizada",
            "severity": "medium"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        alert = Alert.query.filter_by(
            title="Alerta de prueba"
        ).first()

        assert alert is not None
        assert alert.message == "Verificación automatizada"
        assert alert.severity == "medium"


def test_read_alerts(client):
    create_and_login_user(client)

    response = client.get("/alerts/")

    assert response.status_code == 200


def test_resolve_alert(client, app):
    create_and_login_user(client)

    client.post(
        "/alerts/create",
        data={
            "title": "Alerta para resolver",
            "message": "Prueba de resolución",
            "severity": "high"
        }
    )

    with app.app_context():
        alert = Alert.query.filter_by(
            title="Alerta para resolver"
        ).first()
        assert alert is not None
        alert_id = alert.id

    response = client.post(
        f"/alerts/resolve/{alert_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        alert = db_alert = db.session.get(Alert, alert_id)
        assert db_alert is not None
        assert db_alert.status == "resolved"


def test_delete_alert(client, app):
    create_and_login_user(client)

    client.post(
        "/alerts/create",
        data={
            "title": "Alerta para eliminar",
            "message": "Prueba de eliminación",
            "severity": "low"
        }
    )

    with app.app_context():
        alert = Alert.query.filter_by(
            title="Alerta para eliminar"
        ).first()
        assert alert is not None
        alert_id = alert.id

    response = client.post(
        f"/alerts/delete/{alert_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        assert db.session.get(Alert, alert_id) is None



