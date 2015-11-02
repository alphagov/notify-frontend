from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class BaseForm(Form):
    pass


class CreateSMSBatchForm(Form):
    description = StringField('Description', validators=[
        DataRequired(message='Description cannot be empty')
    ])


class InviteUserForm(Form):
    email_address = StringField('Email address', validators=[
        DataRequired(message='Email cannot be empty'),
        Email(message='Please enter a valid email address')
    ])


class ThreeFAForm(Form):
    sms_code = StringField('SMS code', validators=[
        DataRequired(message='SMS cannot be empty'),
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
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message cannot be empty')
    ])
    description = StringField('Description')


class ServiceForm(Form):
    service_name = StringField('Service name', validators=[
        DataRequired(message='Service name is required'),
        Length(min=5, max=160, message="Service name must be between 5 and 160 characters")
    ])
