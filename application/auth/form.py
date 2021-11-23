"""Register & Login Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    """User Registration Form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=30)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=3, max=254)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm your password", validators=[DataRequired(), EqualTo("password")]
    )


class LoginForm(FlaskForm):
    """User Login Form"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
