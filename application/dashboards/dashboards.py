from flask import Blueprint, render_template, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from application.models import db, Dashboard, User, Collection
from .forms import DashboardForm, DashboardSettingsForm

dashboards_bp = Blueprint("dashboards_bp", __name__, template_folder="templates")


@dashboards_bp.route("/create_db", methods=["GET", "POST"])
@login_required
def create_dashboard():
    """Create a new user dashboard"""

    form = DashboardForm()
    if form.validate_on_submit():
        dashboard = Dashboard(
            name=form.name.data,
            description=form.description.data,
            private=form.private.data,
            user_id=current_user.id,
        )
        dashboard.set_slug(form.name.data)

        db.session.add(dashboard)
        db.session.commit()

        return redirect(
            url_for(
                "dashboards_bp.get_dashboard",
                username=current_user.username,
                db_slug=dashboard.slug,
            )
        )

    return render_template("dashboard_create.html.j2", form=form)


@dashboards_bp.route("/<username>/db/<db_slug>")
def get_dashboard(username, db_slug):
    """Get a Users Dashboard"""

    user = User.query.filter_by(username=username).first_or_404()
    dashboard = Dashboard.query.filter_by(user_id=user.id, slug=db_slug).first_or_404()

    return render_template("dashboard.html.j2", user=user, dashboard=dashboard)


@dashboards_bp.route("/<username>/db/<db_slug>/edit", methods=["GET", "POST"])
@login_required
def edit_dashboard(username, db_slug):
    """Render a form and process edits to user dashboards"""

    user = User.query.filter_by(username=username).first_or_404()

    dashboard = Dashboard.query.filter_by(user_id=user.id, slug=db_slug).first_or_404()

    # TODO: Abstract into Decorator
    if current_user.username != username:
        flash("You must own the dashboard to edit it.", "error")
        return redirect(
            url_for("dashboards_bp.get_dashboard", username=username, db_slug=db_slug)
        )

    # Build Form
    form = DashboardSettingsForm(obj=dashboard)
    form.collections.choices = [
        (collection.id, collection.name) for collection in Collection.get_all()
    ]

    # Prepopulate multi-select collections field with existing collections.
    form.collections.data = [c.id for c in dashboard.collections]

    if form.validate_on_submit():
        dashboard.name = form.name.data
        dashboard.set_slug(dashboard.name)
        dashboard.description = form.description.data
        dashboard.private = form.private.data

        collection_ids = form.collections.data
        collections = Collection.query.filter(Collection.id.in_(collection_ids)).all()
        dashboard.collections = collections

        db.session.commit()

        flash("Dashboard Updated.", "message")
        return redirect(
            url_for(
                "dashboards_bp.get_dashboard",
                username=user.username,
                db_slug=dashboard.slug,
            )
        )

    return render_template(
        "dashboard_settings.html.j2", form=form, user=user, dashboard=dashboard
    )
