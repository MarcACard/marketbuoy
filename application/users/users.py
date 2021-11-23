from flask import Blueprint, render_template, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from application.models import db, User, Dashboard
from .forms import UserSettingsForm

users_bp = Blueprint("users_bp", __name__, template_folder="templates")


@users_bp.route("/<username>")
def user_profile(username):
    """User Homepage & Profile"""

    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)

    dashboards = Dashboard.query.filter_by(user_id=user.id).all()

    return render_template("user_profile.html.j2", user=user, dashboards=dashboards)


@users_bp.route("/settings", methods=["GET", "POST"])
@login_required
def user_settings():
    """"""
    user = User.query.filter_by(username=current_user.username).first()

    form = UserSettingsForm(obj=user)

    if form.validate_on_submit():
        user.twitter_id = form.twitter_id.data
        user.bio = form.bio.data
        user.website = form.website.data

        db.session.commit()

        flash("Profile successfully updated.", "message")
        return redirect(url_for("users_bp.user_profile", username=user.username))

    return render_template("user_settings.html.j2", form=form)


@users_bp.route("/settings/delete", methods=["POST"])
@login_required
def delete_user():
    """Delete a user and related dashboards"""

    user = User.query.get_or_404(current_user.id)
    db.session.delete(user)
    db.session.commit()

    flash("User account has been deleted.", "info")

    return redirect(url_for("home_bp.home"))
