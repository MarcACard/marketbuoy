"""Users Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField
from wtforms.validators import URL, Length, Optional


class UserSettingsForm(FlaskForm):
    """User Settings Form."""

    twitter_id = StringField("Twitter", validators=[Length(min=4, max=15)])
    bio = TextAreaField("Bio", validators=[Length(max=160)])
    website = URLField("Website", validators=[URL(), Optional()])
