
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import db
from app.models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# REGISTRO
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "danger")
            return redirect(url_for("auth.register"))

        if confirm_password and password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("El usuario ya existe.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            role="astronaut"
        )

        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()

            flash("Registro exitoso. Ya puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Error al guardar el usuario.", "danger")
            return redirect(url_for("auth.register"))

    # IMPORTANTE: register.html está directamente en templates
    return render_template("register.html")


# INICIO DE SESIÓN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Bienvenido a ASTRA HEALTH.", "success")
            return redirect(url_for("index"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


# CERRAR SESIÓN
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("auth.login"))
