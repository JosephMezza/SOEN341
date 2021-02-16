from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField,
from wtforms.validators import InputRequired, EqualTo, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username_validator = ''  # TODO : regex for valid username (i.e. no special chars)
    username = StringField('Username',
                           validators=[InputRequired(),
                                       Length(4, 32)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(8)])
    password2 = PasswordField('Repeat password',
                              validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Login')

    def validate_password(self, password):
        # TODO : provide password validation criteria
        return True
