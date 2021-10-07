from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo,email_validator


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    email = StringField('E-mail')
    number = IntegerField('Number', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
