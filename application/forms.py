from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Optional, Length, URL


class CollectionForm(FlaskForm):
    slug = StringField("OpenSea Project Slug", validators=[DataRequired()])


class DashboardForm(FlaskForm):
    name = StringField("Dashboard Name", validators=[DataRequired()])
    description = StringField("Dashboard Description", validators=[Optional()])
    private = SelectField("Visibility", choices=[(False, "Public"), (True, "Private")])


class UserProfileForm(FlaskForm):
    twitter_id = StringField("Twitter", validators=[Optional()])
    bio = StringField("Bio", validators=[Optional(), Length(max=160)])
    website = StringField("Website", validators=[Optional(), URL()])
