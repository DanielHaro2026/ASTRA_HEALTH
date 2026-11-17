from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Alert

alerts_bp = Blueprint(
    "alerts",
    __name__,
    url_prefix="/alerts"
)


@alerts_bp.route("/")
@login_required
def index():
    alerts = Alert.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Alert.created_at.desc()
    ).all()

    return render_template("alerts/index.html", alerts=alerts)


@alerts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        message = request.form.get("message", "").strip()
        severity = request.form.get("severity", "").strip()

        if not title or not message:
            flash("Completa el título y el mensaje.", "danger")
            return render_template("alerts/create.html")

        if severity not in ("low", "medium", "high"):
            flash("Selecciona una prioridad válida.", "danger")
            return render_template("alerts/create.html")

        alert = Alert(
            user_id=current_user.id,
            title=title,
            message=message,
            severity=severity,
            status="pending"
        )

        db.session.add(alert)
        db.session.commit()

        flash("Alerta registrada correctamente.", "success")
        return redirect(url_for("alerts.index"))

    return render_template("alerts/create.html")


@alerts_bp.route("/resolve/<int:alert_id>", methods=["POST"])
@login_required
def resolve(alert_id):
    alert = Alert.query.filter_by(
        id=alert_id,
        user_id=current_user.id
    ).first_or_404()

    alert.status = "resolved"
    db.session.commit()

    flash("Alerta marcada como atendida.", "success")
    return redirect(url_for("alerts.index"))


@alerts_bp.route("/delete/<int:alert_id>", methods=["POST"])
@login_required
def delete(alert_id):
    alert = Alert.query.filter_by(
        id=alert_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(alert)
    db.session.commit()

    flash("Alerta eliminada correctamente.", "success")
    return redirect(url_for("alerts.index"))
