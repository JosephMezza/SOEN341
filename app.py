from flask import Flask, session, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, SignUpForm
import bcrypt
import csv

app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# allow the use of @login_required on endpoints which require an account
# unauthenticated users will be redirected to login page

class User(UserMixin):
    def __init__(self, username, email, first_name, last_name, password=None):
        self.id = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return 'User({})'.format(self.id)


@login_manager.user_loader
def load_user(user_id):
    """retrieve a user object for the current user while hiding password"""
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    """ TODO : this will later be changed to searching the database"""
    user = None
    with open('data/users.csv', 'r') as f:
        users = f.readlines()[1:]  # omit header
        for user in users:
            if user[0] == username:
                user = User(*user)
    return user


@app.route('/')
def index():
    """ default app route : probably shouldn't be base.html """
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        valid_password = bcrypt.checkpw(form.password.data.encode(), user.password.encode())
        if user and valid_password:
            login_user(user)
            flash('Log in successful.')
            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """ TODO : This must be changed to searching the database"""
    form = SignUpForm()
    if form.validate_on_submit():
        # check first if user already exists
        user = find_user(form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            with open('data/users.csv', 'w') as f:
                user_data = ','.join(form.username.data, form.email.data, form.first_name.data, form.last_name.data, password.decode())
                f.write(user_data)
            flash('Sign up successful.')
            return redirect('/login')
        else:
            flash('This username already exists')
    return render_template('signup.html', form=form)

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run()
