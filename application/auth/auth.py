from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user
from application.models import db, User
from application import login_manager
from .form import RegistrationForm, LoginForm

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")

############################
# === USER AUTH ROUTES === #
############################


@auth_bp.route("/signup", methods=["GET", "POST"])
def registration():
    """User Sign-up

    GET request returns a registration page
    POST requests validates and processes form submission to create new users
    """
    # TODO: Check for Signed In User

    form = RegistrationForm()

    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_username is not None:
            flash("A user already exists with username")
        elif existing_email is not None:
            flash("A user already exists with this email")
        else:
            user = User(email=form.email.data, username=form.username.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect(url_for("users_bp.user_profile", username=user.username))

    return render_template("registration.html.j2", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User Login

    GET request returns a login page
    POST requests validates credentials and redirects to a user homepage
    """

    # TODO: Check for user login and redirect if logged in

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username.ilike(form.username.data)).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("users_bp.user_profile", username=user.username))

        flash("Invalid Username/Password", "error")

    return render_template("login.html.j2", form=form)


@auth_bp.route("logout")
@login_required
def logout():
    """User Logout"""
    logout_user()
    return redirect(url_for("home_bp.home"))


#########################
# === LOGIN MANAGER === #
#########################


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    print("Load User")
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.", "error")
    return redirect(url_for("auth_bp.login"))
