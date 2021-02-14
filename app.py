from flask import Flask, session, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
import bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# allow the use of @login_required on endpoints which require an account
# unauthenticated users will be redirected to login page

class User(UserMixin):
    def __init__(self, first_name, last_name, username, email, password=None):
        self.id = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return 'User({})'.format(self.id)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = None  # TODO : check that user exists
        password = None  # TODO : check that password matches
        if user and password:
            login_user(user)
            flash('Logged in successfully.')
            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password')
    return render_template('login.html', form=form)


@app.route('/create')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run()
