"""Dashboard Forms"""
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import URL, Length, Optional


class DashboardForm(FlaskForm):
    """Dashboard Creation and Edit Form."""

    name = StringField("Name", validators=[Length(min=4, max=30)])
    description = TextAreaField("Description", validators=[Length(max=160)])
    private = SelectField(
        "Private", choices=[(True, "Private"), ("", "Public")], coerce=bool
    )


class DashboardSettingsForm(DashboardForm):
    """Dashboard Settings Form.
    - Edit Dashboard Fields (name, description, private)
    - Add & Remove Collections
    """

    collections = SelectMultipleField("Collections", coerce=int)
