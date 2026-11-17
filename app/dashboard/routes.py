from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import HealthIndicator, MentalHealthRecord, Alert

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def index():
    total_indicators = HealthIndicator.query.count()

    total_evaluations = MentalHealthRecord.query.filter_by(
        user_id=current_user.id
    ).count()

    pending_alerts = Alert.query.filter_by(
        user_id=current_user.id,
        status="pending"
    ).count()

    resolved_alerts = Alert.query.filter_by(
        user_id=current_user.id,
        status="resolved"
    ).count()

    recent_evaluations = MentalHealthRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(
        MentalHealthRecord.created_at.desc()
    ).limit(5).all()

    recent_alerts = Alert.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Alert.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/index.html",
        total_indicators=total_indicators,
        total_evaluations=total_evaluations,
        pending_alerts=pending_alerts,
        resolved_alerts=resolved_alerts,
        recent_evaluations=recent_evaluations,
        recent_alerts=recent_alerts
    )
