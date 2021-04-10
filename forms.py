from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):

    first_name = StringField('First Name', validators=[InputRequired(),])
    # Regexp('^[a-zA-Z]+$', 0,'First Name must be alphabetic')
    last_name = StringField('Last Name', validators=[InputRequired(),])
    # Regexp('^[a-zA-Z]+$', 0,'Last Name must be alphabetic')
    email = EmailField('Email', validators=[InputRequired(),Email()])
    username = StringField('Username', validators=[InputRequired(), Length(4, 32),])
    # Regexp('^[a-zA-Z0-9._]+', 0,'Username must be alphanumeric and can contain . and _')
    password = PasswordField('Password', validators=[InputRequired(), Length(8),])
    # Regexp('^[a-zA-Z0-9_!]+', 0,'Password must be alphanumeric and can contain ! and _')
    password2 = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class CaptionForm(FlaskForm):
    caption = TextAreaField('Caption', validators=[DataRequired()])
    submit = SubmitField('Done')


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[InputRequired(), Length(8),])
    # Regexp('^[a-zA-Z0-9_!]+', 0, 'Password must be alphanumeric and can contain ! and _')
    password2 = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')
