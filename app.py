from flask import Flask, session, redirect, render_template, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, SignUpForm, CaptionForm, ResetPasswordForm, EmailForm
from user import User
from post import Post, Comment
from datetime import datetime
import bcrypt
import os
import mysql.connector
import emailsend

db_config = {'host': '184.144.173.26',
             'user': 'root',
             'passwd': 'Binstagram_341',
             'database': 'binstagram'
             }
try:
    data_base = mysql.connector.connect(**db_config)
except mysql.connector.errors.InterfaceError:
    db_config['host'] = '192.168.1.53'
    data_base = mysql.connector.connect(**db_config)
finally:
    print(
        f"Successfully connected to db {db_config['database']} on {db_config['host']} with user {db_config['user']}")


app = Flask(__name__)
app.secret_key = 'secret_key'
app.debug = False
# debugging purposes : rollback db on close if False
db_config['commit_to_db'] = not app.debug
app.config["IMAGE_UPLOADS"] = "static/images"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# allow the use of @login_required on endpoints which require an account
# unauthenticated users will be redirected to login page


@login_manager.user_loader
def load_user(user_id):
    """retrieve a user object for the current user while hiding password"""
    user = User.get_from_db(
        data_base, 'id', user_id, commit_to_db=db_config['commit_to_db'])
    if user:
        user.password = None
    return user


@app.route('/')
def index():
    try:
        posts = current_user.get_following_post_images(data_base)
    except:
        posts = None
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get_from_db(data_base, 'username', form.username.data,
                                    hide_password=False, commit_to_db=db_config['commit_to_db'])
            valid_password = bcrypt.checkpw(form.password.data.encode(
                'utf-8'), user.password.encode('utf-8'))
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
                return render_template('main.html')
        except:
            return redirect("/")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # Make loggedIn = False
    session['loggedIn'] = False
    logout_user()
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """Add a user to the database and allow them to sign in"""
    form = SignUpForm()
    if form.validate_on_submit():
        # check first if user already exists
        user = User.get_from_db(
            data_base, 'username', form.username.data, db_config['commit_to_db'])
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            user = User(form.username.data, form.email.data, form.first_name.data,
                        form.last_name.data, password.decode(), commit_to_db=db_config['commit_to_db'])
            user.add_to_db(data_base)
            flash('Sign up successful.')
            return redirect('/login')
        else:
            flash('This username already exists')
    return render_template('signup.html', form=form)
# <img id="unlikebutton" src="..\static\images\unlikebutton.png">


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.get_by_id(data_base, post_id, commit_to_db=db_config['commit_to_db'])
    user = post.get_user(data_base, hide_password=True,
                         commit_to_db=db_config['commit_to_db'])
    user_likes = post.get_user_likes(data_base)
    state = ['like', 'unlike'][current_user.username in user_likes]
    image = post.get_image(data_base)
    comments = Comment.get_post_comments(data_base, post)
    if request.method == 'POST':
        if 'like' in request.form:
            post.like(data_base, current_user)
            return redirect(f"/post/{post_id}")
        if 'unlike' in request.form:
            post.unlike(data_base, current_user)
            return redirect(f"/post/{post_id}")
        if 'comment' in request.form:
            content = request.form.get("comment")
            comment = Comment(current_user.id, post.id, datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), content, commit_to_db=db_config['commit_to_db'])
            comment.add_to_db(data_base)
            return redirect(f"/post/{post_id}")
    return render_template('post.html', post=post, user=user, user_likes=user_likes, state=state, image=image, comments=comments)


@app.route('/users', methods=["GET", "POST"])
def users():
    # dict where username: follow_state
    users = current_user.get_followable(data_base)
    if request.method == 'POST':
        if 'follow' in request.form:
            username = request.form.get('follow')
            user = User.get_from_db(
                data_base, 'username', username, db_config['commit_to_db'])
            current_user.follow(data_base, user)
        if 'unfollow' in request.form:
            username = request.form.get('unfollow')
            user = User.get_from_db(
                data_base, 'username', username, db_config['commit_to_db'])
            current_user.unfollow(data_base, user)
        return redirect("/users")
    return render_template('users.html', users=users)


@app.route('/profile/<username>', methods=["GET", "POST"])
def profile(username):
    user = User.get_from_db(data_base, 'username', username,
                            db_config['commit_to_db'])
    posts = user.get_post_images(data_base)
    likes = user.get_likes(data_base)
    followers = list(map(lambda x: x.username, user.get_followers(data_base)))
    following = list(map(lambda x: x.username, user.get_following(data_base)))
    return render_template('profile.html', user=user, posts=posts, likes=likes, followers=followers, following=following)


@app.route('/upload-image', methods=["GET", "POST"])
def postimage():
    if request.method == "POST":
        try:
            if request.files:
                image_file = request.files["image"]
                file_name = image_file.filename
                file_path = f'{app.config["IMAGE_UPLOADS"]}/{file_name}'
                extension = file_name[file_name.rindex('.') + 1:].lower()
                if extension in ("png", "jpg", "gif"):
                    image_file.save(file_path)
                    post = Post(current_user.id, datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), commit_to_db=db_config['commit_to_db'])
                    post_id = post.add_to_db(data_base, file_path)
                    os.remove(file_path)
                    return redirect(f"/caption/{post_id}")
                else:
                    print('invalid file')
                    return redirect("/upload-image")
        except Exception as e:
            print(e)
            return redirect("/upload-image")
    return render_template("upload-image.html")


@app.route('/caption/<post_id>', methods=["GET", "POST"])
def post_caption(post_id):
    post = Post.get_by_id(data_base, post_id, commit_to_db=db_config['commit_to_db'])
    image = post.get_image(data_base)
    form = CaptionForm()
    if request.method == "POST":
        caption = form.caption.data
        post.change_caption(data_base, caption)
        return redirect(f"/post/{post_id}")
    return render_template('caption.html', form=form, image=image)


@app.route('/forgotPassword', methods=["GET", "POST"])
def forgotPassword():
    form = EmailForm()
    if request.method == "POST":
        email = form.email.data
        print(email)
        link = "http://127.0.0.1:5000/resetPassword/"+email
        emailsend.send_email(email, link)
        return redirect("/")
    return render_template('forgotPassword.html', form=form)


@app.route('/resetPassword/<emailadress>', methods=["GET", "POST"])
def ResetPassword(emailadress):
    form = ResetPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # gets information of password from form
            password = form.password.data
            password2 = form.password2.data
            # checks to see if password is good
            if password != password2:
                return redirect("/resetPassword/"+emailadress)
            user = User.get_from_db(data_base, 'email', emailadress)
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                form.password.data.encode('utf-8'), salt)
            user.change_password(data_base, hashed_password)
            return redirect("/")
    return render_template('resetPassword.html', form=form, emailadress=emailadress)


def main(commit_to_db=True):
    if not commit_to_db:
        cursor = data_base.cursor()
        cursor.execute("START TRANSACTION")
        cursor.close()
    app.run()
    if not commit_to_db:
        cursor = data_base.cursor()
        cursor.execute("ROLLBACK")
        cursor.close()
    data_base.close()


if __name__ == '__main__':
    main(commit_to_db=db_config['commit_to_db'])
