from flask import Flask, session, redirect, render_template, flash, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, SignUpForm
import bcrypt
import csv
import follower

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
    users = follower.getListFromCSV('data/users.csv')
    for user in users[1:]:
        if user[0] == username:
            return User(*user)
    return None


@app.route('/')
def index():
    imageList = follower.getImagesToShow("Marknow") # eventually change to logged in user

    # """ default app route : probably shouldn't be base.html """
    # session['loggedIn'] = None  # TODO : remove this
    # print(session)
    
    return render_template('main.html', imageList=imageList, loggedIn=session['loggedIn'])

# Test User:
# Calasts53
# eeG1fior0g
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        valid_password = form.password.data == user.password
        # valid_password = bcrypt.checkpw(form.password.data.encode(), user.password.encode())
        if user and valid_password:
            session['loggedIn'] = True
            login_user(user)
            flash('Log in successful.')
            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            return redirect(next_page)
        else:
            session['loggedIn'] = False
            flash('Incorrect username/password')
    return render_template('login.html', form=form, loggedIn=session['loggedIn'])


@app.route('/logout')
@login_required
def logout():
    # Make loggedIn = False
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


@app.route('/users' , methods=["GET","POST"])
def users():
    usersList = follower.getusers()
    if request.method == 'POST':
        userToFollow = request.form.get('follow')
        print(userToFollow)
        follower.follow("Marknow", userToFollow)
        return redirect("/")
    return render_template('users.html', usersList = usersList)

if __name__ == '__main__':
    app.run()
