from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class InviteUserForm(Form):
    email_address = StringField('Email address', validators=[
        DataRequired(message='Email cannot be empty'),
        Email(message='Please enter a valid email address')
    ])


class LoginForm(Form):
    email_address = StringField('Email address', validators=[
        DataRequired(message='Email cannot be empty'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password')
    ])


class RegistrationForm(Form):
    name = StringField('Name', validators=[
        DataRequired(message='Email cannot be empty')
    ])
    email_address = StringField('Email address', validators=[
        DataRequired(message='Email cannot be empty'),
        Email(message='Please enter a valid email address')
    ])
    mobile_number = StringField('Mobile number', validators=[
        DataRequired(message='Mobile number cannot be empty')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password')
    ])


class SmsForm(Form):
    mobile_number = StringField('Mobile number', validators=[
        DataRequired(message='Mobile number cannot be empty')
    ])
    message = StringField('Message', validators=[
        DataRequired(message='Message cannot be empty')
    ])


class ServiceForm(Form):
    service_name = StringField('Service name', validators=[
        DataRequired(message='Service name is required')
    ])
