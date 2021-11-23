"""Home Page"""
from flask import Blueprint, render_template

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/")
def home():
    """Website Homepage"""

    # TODO: Import Home Page Dashboard.

    return render_template("home.html.j2")
