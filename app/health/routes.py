
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from flask_login import login_required
from app.extensions import db
from app.models import HealthIndicator

health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/health"
)


@health_bp.route("/")
@login_required
def index():
    indicators = HealthIndicator.query.order_by(
        HealthIndicator.created_at.desc()
    ).all()

    return render_template(
        "health/index.html",
        indicators=indicators
    )


@health_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        value = request.form.get("value", "").strip()
        unit = request.form.get("unit", "").strip()
        description = request.form.get("description", "").strip()

        if not all([name, category, value, unit]):
            flash("Completa todos los campos obligatorios.", "danger")
            return render_template("health/create.html")

        try:
            numeric_value = float(value)
        except ValueError:
            flash("El valor debe ser numérico.", "danger")
            return render_template("health/create.html")

        indicator = HealthIndicator(
            name=name,
            category=category,
            value=numeric_value,
            unit=unit,
            description=description or None
        )

        db.session.add(indicator)
        db.session.commit()

        flash("Indicador registrado correctamente.", "success")
        return redirect(url_for("health.index"))

    return render_template("health/create.html")


@health_bp.route("/edit/<int:indicator_id>", methods=["GET", "POST"])
@login_required
def edit(indicator_id):
    indicator = db.get_or_404(HealthIndicator, indicator_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        value = request.form.get("value", "").strip()
        unit = request.form.get("unit", "").strip()
        description = request.form.get("description", "").strip()

        if not all([name, category, value, unit]):
            flash("Completa todos los campos obligatorios.", "danger")
            return render_template(
                "health/edit.html",
                indicator=indicator
            )

        try:
            indicator.value = float(value)
        except ValueError:
            flash("El valor debe ser numérico.", "danger")
            return render_template(
                "health/edit.html",
                indicator=indicator
            )

        indicator.name = name
        indicator.category = category
        indicator.unit = unit
        indicator.description = description or None

        db.session.commit()

        flash("Indicador actualizado correctamente.", "success")
        return redirect(url_for("health.index"))

    return render_template(
        "health/edit.html",
        indicator=indicator
    )


@health_bp.route("/delete/<int:indicator_id>", methods=["POST"])
@login_required
def delete(indicator_id):
    indicator = db.get_or_404(HealthIndicator, indicator_id)

    db.session.delete(indicator)
    db.session.commit()

    flash("Indicador eliminado correctamente.", "success")
    return redirect(url_for("health.index"))
