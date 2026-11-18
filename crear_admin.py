
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    username = "admin"
    email = "diharove@gmail.com"

    existente = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existente:
        print("El usuario o correo ya existe.")
    else:
        password = input("Escribe tu nueva contraseña: ")

        if len(password) >= 8:
            usuario = User(
                username=username,
                email=email,
                role="admin"
            )
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            print("ADMINISTRADOR CREADO CORRECTAMENTE")
        else:
            print("La contraseña debe tener al menos 8 caracteres.")
