from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField, DateTimeField, SelectField, IntegerField, EmailField


class BirthdayForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    date = DateTimeField('Date of birth:', format='%d.%m.%Y')
    presents = StringField('Presents:', validators=[DataRequired()])
    submit = SubmitField('Save')


class ChangeForm(FlaskForm):
    name = StringField('')
    date = StringField('')
    presents = StringField('')
    submit = SubmitField('Save')


class RegistrationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    surname = StringField('Surname:', validators=[DataRequired()])
    age = IntegerField('Age:')
    email = EmailField('Login or email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password_again = PasswordField('Repeat password:', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Login or email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Enter')