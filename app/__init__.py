
import os

from flask import Flask, render_template

from config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):

    # =================================================
    # CREAR APLICACIÃ“N FLASK
    # =================================================

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    # =================================================
    # INICIALIZAR EXTENSIONES
    # =================================================

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Inicia sesiÃ³n para continuar."
    login_manager.login_message_category = "warning"

    # =================================================
    # IMPORTAR MODELOS
    # =================================================

    from app.models import User, HealthIndicator

    # =================================================
    # CARGADOR DE USUARIOS FLASK-LOGIN
    # =================================================

    @login_manager.user_loader
    def load_user(user_id):

        try:
            return db.session.get(
                User,
                int(user_id)
            )

        except (ValueError, TypeError):
            return None

    # =================================================
    # REGISTRAR BLUEPRINT DE AUTENTICACIÃ“N
    # =================================================

    from app.auth.routes import auth_bp

    app.register_blueprint(auth_bp)

    # =================================================
    # REGISTRAR BLUEPRINT DE SALUD
    # =================================================

    from app.health.routes import health_bp

    app.register_blueprint(health_bp)
    # REGISTRAR BLUEPRINT DE SALUD MENTAL
    from app.mental_health.routes import mental_health_bp
    app.register_blueprint(mental_health_bp)
    # REGISTRAR BLUEPRINT DE ALERTAS
    from app.alerts.routes import alerts_bp
    app.register_blueprint(alerts_bp)
    # REGISTRAR BLUEPRINT DEL DASHBOARD
    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    # REGISTRAR BLUEPRINT ADMIN
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    # =================================================
    # CREAR TABLAS DE BASE DE DATOS
    # =================================================

    with app.app_context():
        db.create_all()

    # =================================================
    # PÃGINA PRINCIPAL
    # =================================================

    @app.route("/")
    def index():

        return render_template("index.html")

    return app




