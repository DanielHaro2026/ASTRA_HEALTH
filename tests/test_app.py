
from app.extensions import db
from app.models import HealthIndicator, User


def register_and_login(client):
    """Crea un usuario de prueba e inicia su sesión."""

    client.post(
        "/auth/register",
        data={
            "username": "astronaut_test",
            "email": "astronaut@test.com",
            "password": "Astronaut123!"
        },
        follow_redirects=True
    )

    response = client.post(
        "/auth/login",
        data={
            "email": "astronaut@test.com",
            "password": "Astronaut123!"
        },
        follow_redirects=True
    )

    return response


def create_test_indicator(client):
    """Registra un indicador de prueba."""

    return client.post(
        "/health/create",
        data={
            "name": "Frecuencia cardíaca",
            "category": "Physical Health",
            "value": "75",
            "unit": "bpm",
            "description": "Medición de prueba en reposo"
        },
        follow_redirects=True
    )


# =====================================================
# PRUEBAS DE LA PÁGINA PRINCIPAL
# =====================================================

def test_homepage_status(client):
    response = client.get("/")

    assert response.status_code == 200


def test_homepage_content(client):
    response = client.get("/")

    assert b"ASTRA HEALTH" in response.data


def test_homepage_language(client):
    response = client.get("/")

    assert b"astronaut health monitoring" in response.data.lower()


# =====================================================
# PRUEBAS DE AUTENTICACIÓN Y PROTECCIÓN
# =====================================================

def test_health_requires_login(client):
    response = client.get("/health/")

    assert response.status_code in (302, 401)


# =====================================================
# PRUEBA CREATE: REGISTRAR INDICADOR
# =====================================================

def test_create_health_indicator(client, app):
    register_and_login(client)

    response = create_test_indicator(client)

    assert response.status_code == 200
    assert b"Frecuencia card" in response.data

    with app.app_context():
        indicator = HealthIndicator.query.filter_by(
            name="Frecuencia cardíaca"
        ).first()

        assert indicator is not None
        assert indicator.value == 75.0
        assert indicator.unit == "bpm"


# =====================================================
# PRUEBA READ: CONSULTAR INDICADORES
# =====================================================

def test_read_health_indicators(client):
    register_and_login(client)
    create_test_indicator(client)

    response = client.get("/health/")

    assert response.status_code == 200
    assert b"Frecuencia card" in response.data


# =====================================================
# PRUEBA UPDATE: EDITAR INDICADOR
# =====================================================

def test_update_health_indicator(client, app):
    register_and_login(client)
    create_test_indicator(client)

    with app.app_context():
        indicator = HealthIndicator.query.filter_by(
            name="Frecuencia cardíaca"
        ).first()

        indicator_id = indicator.id

    response = client.post(
        f"/health/edit/{indicator_id}",
        data={
            "name": "Frecuencia cardíaca",
            "category": "Physical Health",
            "value": "80",
            "unit": "bpm",
            "description": "Medición actualizada"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        indicator = db.session.get(
            HealthIndicator,
            indicator_id
        )

        assert indicator.value == 80.0
        assert indicator.description == "Medición actualizada"


# =====================================================
# PRUEBA DELETE: ELIMINAR INDICADOR
# =====================================================

def test_delete_health_indicator(client, app):
    register_and_login(client)
    create_test_indicator(client)

    with app.app_context():
        indicator = HealthIndicator.query.filter_by(
            name="Frecuencia cardíaca"
        ).first()

        indicator_id = indicator.id

    response = client.post(
        f"/health/delete/{indicator_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        indicator = db.session.get(
            HealthIndicator,
            indicator_id
        )

        assert indicator is None


# =====================================================
# PRUEBA DE VALIDACIÓN
# =====================================================

def test_create_indicator_with_invalid_value(client, app):
    register_and_login(client)

    response = client.post(
        "/health/create",
        data={
            "name": "Frecuencia cardíaca",
            "category": "Physical Health",
            "value": "texto incorrecto",
            "unit": "bpm",
            "description": "Prueba de validación"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"El valor debe ser num" in response.data

    with app.app_context():
        indicator = HealthIndicator.query.filter_by(
            name="Frecuencia cardíaca"
        ).first()

        assert indicator is None

from app.models import MentalHealthRecord

# =====================================================
# PRUEBAS DEL MODULO MENTAL HEALTH
# =====================================================

def test_create_mental_health_record(client, app):
    register_and_login(client)

    response = client.post(
        "/mental-health/create",
        data={
            "mood": "Bien",
            "stress_level": "4",
            "sleep_hours": "7.5",
            "notes": "Evaluación de prueba"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Evaluación registrada correctamente.".encode() in response.data

    with app.app_context():
        record = MentalHealthRecord.query.filter_by(
            mood="Bien"
        ).first()

        assert record is not None
        assert record.stress_level == 4
        assert record.sleep_hours == 7.5
        assert record.notes == "Evaluación de prueba"


def test_read_mental_health_records(client):
    register_and_login(client)

    client.post(
        "/mental-health/create",
        data={
            "mood": "Neutral",
            "stress_level": "5",
            "sleep_hours": "8",
            "notes": "Consulta de prueba"
        },
        follow_redirects=True
    )

    response = client.get("/mental-health/")

    assert response.status_code == 200
    assert b"Neutral" in response.data
    assert b"Consulta de prueba" in response.data


def test_update_mental_health_record(client, app):
    register_and_login(client)

    client.post(
        "/mental-health/create",
        data={
            "mood": "Bien",
            "stress_level": "4",
            "sleep_hours": "7",
            "notes": "Registro inicial"
        },
        follow_redirects=True
    )

    with app.app_context():
        record = MentalHealthRecord.query.filter_by(
            mood="Bien"
        ).first()
        record_id = record.id

    response = client.post(
        f"/mental-health/edit/{record_id}",
        data={
            "mood": "Muy bien",
            "stress_level": "2",
            "sleep_hours": "8",
            "notes": "Registro actualizado"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        record = db.session.get(MentalHealthRecord, record_id)

        assert record.mood == "Muy bien"
        assert record.stress_level == 2
        assert record.sleep_hours == 8.0
        assert record.notes == "Registro actualizado"


def test_delete_mental_health_record(client, app):
    register_and_login(client)

    client.post(
        "/mental-health/create",
        data={
            "mood": "Neutral",
            "stress_level": "5",
            "sleep_hours": "7",
            "notes": "Registro para eliminar"
        },
        follow_redirects=True
    )

    with app.app_context():
        record = MentalHealthRecord.query.filter_by(
            notes="Registro para eliminar"
        ).first()
        record_id = record.id

    response = client.post(
        f"/mental-health/delete/{record_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        record = db.session.get(MentalHealthRecord, record_id)
        assert record is None


def test_mental_health_rejects_invalid_stress(client, app):
    register_and_login(client)

    response = client.post(
        "/mental-health/create",
        data={
            "mood": "Bien",
            "stress_level": "15",
            "sleep_hours": "7",
            "notes": "Prueba de validación"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"El estr" in response.data

    with app.app_context():
        record = MentalHealthRecord.query.filter_by(
            notes="Prueba de validación"
        ).first()

        assert record is None

