# Register forms 
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, StringField  
from wtforms.validators import DataRequired, Length
# what does Flaskform do?
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=
    [
    DataRequired(message='Username is required'),
    Length(min=1, max=25),
    ])

    email = StringField('Email', validators=
    [
    DataRequired('Email is required'),
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    ])


    password = PasswordField('Password', validators=
    [
    DataRequired('Password is required'), 
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    ])

    confirm_password = PasswordField('Repeat Password', validators=
    [
    DataRequired('Does not match password'),
    ])


class LoginForm(FlaskForm):
    #'todo implement Username_or_email'
    username = StringField('Username', validators=[DataRequired('Username is required')],)  
    password = PasswordField('Password', validators=[DataRequired('Password is required'),])