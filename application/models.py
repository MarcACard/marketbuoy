from . import db
from sqlalchemy import func
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt()


class Collection(db.Model):
    """NFT Collections Model"""

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    banner_image_url = db.Column(db.String)
    created_date = db.Column(db.DateTime)
    description = db.Column(db.String)
    name = db.Column(db.String, unique=True)
    slug = db.Column(db.String, unique=True)
    telegram_url = db.Column(db.String)
    twitter_username = db.Column(db.String)
    instagram_username = db.Column(db.String)
    wiki_url = db.Column(db.String)
    discord_url = db.Column(db.String)
    image_url = db.Column(db.String)
    # TODO: FIX - last update column should update each time the record is updated.
    last_updated = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Collection | name: {self.name}>"

    @classmethod
    def get_all(cls):
        """Return all Collections."""
        return cls.query.all()

    @classmethod
    def get_one(cls, slug):
        """Return a single collection.

        Args:
            slug (str) - a slug in reference to a specific collection

        Returns:
            Collection record, or None.
        """
        return cls.query.filter_by(slug=slug).first()


class CollectionDashboard(db.Model):
    """Collection Dashboard Model"""

    __tablename__ = "collections_dashboards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id"), nullable=False)
    collection_id = db.Column(
        db.Integer, db.ForeignKey("collections.id"), nullable=False
    )


class Dashboard(db.Model):
    """Dashboard Model"""

    __tablename__ = "dashboards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    private = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    collections = db.relationship(
        "Collection", secondary="collections_dashboards", backref="dashboards"
    )

    def set_slug(self, name):
        """Generate a Dashboard's URL Slug

        Generate a URL safe slug through modifying the dashboard name with regex.

        Regex Note:
            Reference: https://stackoverflow.com/questions/2627523/replace-all-spaces-and-special-symbols-with-dash-in-url-using-php-language
            1 - Remove all characters except Letters & Numbers & Replace with a '-'
            2 - Remove trailing '-' if they exist

        Args:
            name (str): Name of a Dashboard.
        """

        safe_string = re.sub("[^a-zA-Z0-9]+", "-", name)
        slug = re.sub("([-]*)$", "", safe_string)

        self.slug = slug

    def __repr__(self):
        return f"<Dashboard | name: {self.name}, user_id: {self.user_id}>"


class User(UserMixin, db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    twitter_id = db.Column(db.String(15))
    bio = db.Column(db.String(160))
    website = db.Column(db.String)

    dashboards = db.relationship("Dashboard", cascade="all, delete", backref="user")

    def set_password(self, password):
        """Created a hashed password"""
        hashed_pw = bcrypt.generate_password_hash(password)
        self.password = hashed_pw.decode("utf8")

    def check_password(self, password):
        """Check password against hashed password

        Args:
            password (str) - A password.

        Returns:
            True if password matches hash. Otherwise False

        """

        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User | username: {self.username}>"


class CollectionStats(db.Model):
    """Collection Stats Model"""

    __tablename__ = "collection_stats"

    id = db.Column(db.Integer, primary_key=True)
    # Date/Time Record
    # Floor Price

    # relationship w/ collection

    # @Static Method - get_todays_floor (Collection) return current floor, yesterday floor, % change in an object
