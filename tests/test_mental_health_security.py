from app.extensions import db
from app.models.user import User
from app.models import MentalHealthRecord


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


def test_user_cannot_access_another_users_mental_health_record(
    client, app
):
    # Usuario A crea una evaluación privada
    register_and_login(
        client, "astronaut_a", "astronaut_a@test.com"
    )

    client.post(
        "/mental-health/create",
        data={
            "mood": "Calmado",
            "stress_level": "3",
            "sleep_hours": "8",
            "notes": "PRIVATE_NOTE_USER_A"
        }
    )

    with app.app_context():
        user_a = User.query.filter_by(
            username="astronaut_a"
        ).first()

        record = MentalHealthRecord.query.filter_by(
            user_id=user_a.id
        ).first()

        assert record is not None
        record_id = record.id
        user_a_id = user_a.id

    # Usuario A cierra sesión y entra Usuario B
    client.get("/auth/logout")

    register_and_login(
        client, "astronaut_b", "astronaut_b@test.com"
    )

    # B no debe ver la evaluación privada de A
    response = client.get("/mental-health/")
    assert response.status_code == 200
    assert b"PRIVATE_NOTE_USER_A" not in response.data

    # B no puede consultar ni modificar la evaluación de A
    response = client.get(
        f"/mental-health/edit/{record_id}"
    )
    assert response.status_code == 404

    response = client.post(
        f"/mental-health/edit/{record_id}",
        data={
            "mood": "Alterado",
            "stress_level": "10",
            "sleep_hours": "2",
            "notes": "Intento de modificación"
        }
    )
    assert response.status_code == 404

    # B tampoco puede eliminar la evaluación de A
    response = client.post(
        f"/mental-health/delete/{record_id}"
    )
    assert response.status_code == 404

    # Comprobar que el registro original sigue intacto
    with app.app_context():
        record = db.session.get(
            MentalHealthRecord, record_id
        )

        assert record is not None
        assert record.user_id == user_a_id
        assert record.notes == "PRIVATE_NOTE_USER_A"
        assert record.mood == "Calmado"
