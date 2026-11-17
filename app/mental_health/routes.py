from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import MentalHealthRecord

mental_health_bp = Blueprint(
    "mental_health",
    __name__,
    url_prefix="/mental-health"
)


@mental_health_bp.route("/")
@login_required
def index():
    records = MentalHealthRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(
        MentalHealthRecord.created_at.desc()
    ).all()

    return render_template(
        "mental_health/index.html",
        records=records
    )


@mental_health_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        mood = request.form.get("mood", "").strip()
        stress = request.form.get("stress_level", "").strip()
        sleep = request.form.get("sleep_hours", "").strip()
        notes = request.form.get("notes", "").strip()

        if not mood or not stress or not sleep:
            flash("Completa todos los campos obligatorios.", "danger")
            return render_template("mental_health/create.html")

        try:
            stress_level = int(stress)
            sleep_hours = float(sleep)

            if not 1 <= stress_level <= 10:
                raise ValueError

            if not 0 <= sleep_hours <= 24:
                raise ValueError

        except ValueError:
            flash(
                "El estrés debe estar entre 1 y 10 y el sueño entre 0 y 24 horas.",
                "danger"
            )
            return render_template("mental_health/create.html")

        record = MentalHealthRecord(
            user_id=current_user.id,
            mood=mood,
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            notes=notes or None
        )

        db.session.add(record)
        db.session.commit()

        flash("Evaluación registrada correctamente.", "success")
        return redirect(url_for("mental_health.index"))

    return render_template("mental_health/create.html")


@mental_health_bp.route("/edit/<int:record_id>", methods=["GET", "POST"])
@login_required
def edit(record_id):
    record = MentalHealthRecord.query.filter_by(
        id=record_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        mood = request.form.get("mood", "").strip()
        stress = request.form.get("stress_level", "").strip()
        sleep = request.form.get("sleep_hours", "").strip()
        notes = request.form.get("notes", "").strip()

        if not mood or not stress or not sleep:
            flash("Completa todos los campos obligatorios.", "danger")
            return render_template(
                "mental_health/edit.html",
                record=record
            )

        try:
            stress_level = int(stress)
            sleep_hours = float(sleep)

            if not 1 <= stress_level <= 10:
                raise ValueError

            if not 0 <= sleep_hours <= 24:
                raise ValueError

        except ValueError:
            flash(
                "El estrés debe estar entre 1 y 10 y el sueño entre 0 y 24 horas.",
                "danger"
            )
            return render_template(
                "mental_health/edit.html",
                record=record
            )

        record.mood = mood
        record.stress_level = stress_level
        record.sleep_hours = sleep_hours
        record.notes = notes or None

        db.session.commit()

        flash("Evaluación actualizada correctamente.", "success")
        return redirect(url_for("mental_health.index"))

    return render_template(
        "mental_health/edit.html",
        record=record
    )


@mental_health_bp.route("/delete/<int:record_id>", methods=["POST"])
@login_required
def delete(record_id):
    record = MentalHealthRecord.query.filter_by(
        id=record_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(record)
    db.session.commit()

    flash("Evaluación eliminada correctamente.", "success")
    return redirect(url_for("mental_health.index"))
