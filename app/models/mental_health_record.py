
from datetime import datetime, timezone

from app.extensions import db


class MentalHealthRecord(db.Model):
    __tablename__ = "mental_health_records"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    mood = db.Column(
        db.String(50),
        nullable=False
    )

    stress_level = db.Column(
        db.Integer,
        nullable=False
    )

    sleep_hours = db.Column(
        db.Float,
        nullable=False
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "mental_health_records",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<MentalHealthRecord {self.id}>"
