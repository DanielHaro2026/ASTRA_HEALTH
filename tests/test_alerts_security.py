from app.extensions import db
from app.models.user import User
from app.models import Alert


def register_and_login(client, username, email):
    response = client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": "Password123"
        }
    )
    assert response.status_code == 302

    response = client.post(
        "/auth/login",
        data={
            "email": email,
            "password": "Password123"
        }
    )
    assert response.status_code == 302


def test_user_cannot_access_another_users_alert(client, app):
    # Usuario A crea una alerta privada
    register_and_login(
        client, "alert_owner", "alert_owner@test.com"
    )

    client.post(
        "/alerts/create",
        data={
            "title": "ALERTA_PRIVADA_A",
            "message": "Mensaje privado del usuario A",
            "severity": "high"
        }
    )

    with app.app_context():
        owner = User.query.filter_by(
            username="alert_owner"
        ).first()

        alert = Alert.query.filter_by(
            user_id=owner.id
        ).first()

        assert alert is not None
        alert_id = alert.id
        owner_id = owner.id

    # Usuario A cierra sesión y entra Usuario B
    client.get("/auth/logout")

    register_and_login(
        client, "alert_intruder", "alert_intruder@test.com"
    )

    # B no debe visualizar la alerta de A
    response = client.get("/alerts/")

    assert response.status_code == 200
    assert b"ALERTA_PRIVADA_A" not in response.data

    # B no puede resolver la alerta de A
    response = client.post(f"/alerts/resolve/{alert_id}")
    assert response.status_code == 404

    # B no puede eliminar la alerta de A
    response = client.post(f"/alerts/delete/{alert_id}")
    assert response.status_code == 404

    # Comprobar que la alerta original sigue intacta
    with app.app_context():
        alert = db.session.get(Alert, alert_id)

        assert alert is not None
        assert alert.user_id == owner_id
        assert alert.title == "ALERTA_PRIVADA_A"
        assert alert.status == "pending"
