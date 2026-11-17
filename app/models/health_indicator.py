
from datetime import datetime, timezone

from app.extensions import db


class HealthIndicator(db.Model):
    __tablename__ = "health_indicators"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)

    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(30), nullable=False)

    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<HealthIndicator {self.name}>"
