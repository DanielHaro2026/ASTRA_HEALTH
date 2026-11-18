import os
import sys

from app import create_app
from app.extensions import db
from app.models import User

CUENTAS = [
    {
        "username": "daniel_haro",
        "email": "diharov@hotmail.com",
        "role": "admin",
        "env": "ASTRA_ADMIN1_PASSWORD",
    },
    {
        "username": "admin",
        "email": "diharove@gmail.com",
        "role": "admin",
        "env": "ASTRA_ADMIN2_PASSWORD",
    },
    {
        "username": "32033883",
        "email": "diharovega@gmail.com",
        "role": "astronaut",
        "env": "ASTRA_ASTRONAUT_PASSWORD",
    },
]


def inicializar():
    app = create_app()

    with app.app_context():
        db.create_all()

        for cuenta in CUENTAS:
            usuario = User.query.filter_by(
                username=cuenta["username"]
            ).first()

            usuario_email = User.query.filter_by(
                email=cuenta["email"]
            ).first()

            if usuario and usuario.email != cuenta["email"]:
                raise ValueError(
                    f"El usuario {cuenta['username']} tiene otro correo."
                )

            if usuario_email and usuario_email.username != cuenta["username"]:
                raise ValueError(
                    f"El correo {cuenta['email']} pertenece a otra cuenta."
                )

            if usuario:
                print(f"YA EXISTE, SE CONSERVA: {cuenta['username']}")
                continue

            password = os.environ.get(cuenta["env"])

            if not password or len(password) < 12:
                raise ValueError(
                    f"Falta {cuenta['env']} o tiene menos de 12 caracteres."
                )

            usuario = User(
                username=cuenta["username"],
                email=cuenta["email"],
                role=cuenta["role"],
            )
            usuario.set_password(password)
            db.session.add(usuario)

            print(f"CREADO: {cuenta['username']}")

        db.session.commit()
        print("Inicialización finalizada correctamente.")


if __name__ == "__main__":
    try:
        inicializar()
    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)
