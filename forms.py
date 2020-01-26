from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)

from models import User


# this method will check if the email already exists
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


'''FORM FOR REGISTERING'''


class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]'
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[
            DataRequired()
        ]
    )


'''FORM FOR LOGIN'''


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )


'''FORM FOR SEARCH'''


class FlightSearchForm(FlaskForm):
    form_date = StringField(
        'Date',
        validators=[
            DataRequired()
        ]
    )
    form_origin = StringField(
        'From',
        validators=[
            DataRequired()
        ]
    )
    form_destination = StringField(
        'To',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Search')


'''FORM TO REMOVE FLIGHT'''


class RemoveFlightForm(FlaskForm):
    flight_number = StringField("Flight Number")
    remove = SubmitField('Remove Flight')
