from functools import wraps

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from app.models import User

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if getattr(current_user, "role", None) != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


@admin_bp.route("/")
@admin_required
def index():
    users = User.query.order_by(User.id.desc()).all()

    total_users = len(users)
    total_admins = sum(
        1 for user in users if user.role == "admin"
    )
    total_astronauts = sum(
        1 for user in users if user.role == "astronaut"
    )

    return render_template(
        "admin/index.html",
        users=users,
        total_users=total_users,
        total_admins=total_admins,
        total_astronauts=total_astronauts
    )
