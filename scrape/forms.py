from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class ScrapeForm(FlaskForm):
    domain = StringField('Scrape from indeed',
                           validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country',
                           validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Scrape')
