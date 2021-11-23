from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Initialize core application."""
    app = Flask(__name__, instance_relative_config=False)

    # App Configuration
    # TODO: Fix configuration loading. Doesn't seem all settings are registering.
    app.config.from_object("config.Config")

    # Initialize Plugins
    db.init_app(app)  # SQLAlchemy
    login_manager.init_app(app)

    with app.app_context():
        # Add Routes
        from . import home
        from .auth import auth
        from .collections import collections
        from .users import users
        from .dashboards import dashboards

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(auth.auth_bp, url_prefix="/auth")
        app.register_blueprint(collections.collections_bp, url_prefix="/collections")
        app.register_blueprint(users.users_bp, url_prefix="/u")
        app.register_blueprint(dashboards.dashboards_bp, url_prefix="/u")

        # Todo: Fix this
        # db.drop_all()
        # db.create_all()

        return app
