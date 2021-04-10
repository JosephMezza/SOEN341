from flask import Flask, session, redirect, render_template, flash, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from forms import LoginForm, SignUpForm, CaptionForm, ResetPasswordForm, EmailForm
from werkzeug.utils import secure_filename
from user import User
from post import Post
from re import I
import bcrypt
import tornado.web
import tornado.ioloop
import os
import mysql.connector
import emailsend

db_config = {'host': '184.144.173.26',
          'user': 'root',
          'passwd': 'Binstagram_341',
          'database': 'binstagram'
          }

try:
    db = mysql.connector.connect(**db_config)
except mysql.connector.errors.InterfaceError:
    db_config['host'] = '192.168.1.53'
    db = mysql.connector.connect(**db_config)
finally:
    print('Successfully connected to db {} on {} with user {}'.format(db_config['database'], db_config['host'], db_config['user']))


app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# allow the use of @login_required on endpoints which require an account
# unauthenticated users will be redirected to login page


@login_manager.user_loader
def load_user(user_id):
    """retrieve a user object for the current user while hiding password"""
    user = User.getUser(db, 'id', user_id)
    if user:
        user.pop()
    return user.User(*user)


@app.route('/')
def index():
    username = "Calasts53"
    imageList = []
    try:
        username = str(session['_user_id'])
        imageList = User.getImagesToShow(db, username)
        imagedict = {imageList[index * 2 + 1]: imageList[index * 2] for index in len(imageList) / 2 - 5}
        print(imagedict)
    except:
        print("An exception occurred")
        username = "Calasts53"
    return render_template('main.html', imageList=imageList)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.getUserByUsername(db, form.username.data)
            valid_password = bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8'))
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
    return render_template('login.html', form=form, )


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
    """ TODO : This must be changed to searching the database"""
    form = SignUpForm()
    if form.validate_on_submit():
        # check first if user already exists
        user = User.get_user(db, form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            User.addUser(db, form.username.data, password.decode(), form.email.data, form.first_name.data, form.last_name.data)
            flash('Sign up successful.')
            return redirect('/login')
        else:
            flash('This username already exists')
    return render_template('signup.html', form=form)


@app.route('/post/<image>', methods=['GET', 'POST'])
def post(image):
    id = int(Post.getID(db, image))
    postList = Post.getInfo(db, id)
    if request.method == 'POST' and 'like' in request.form:
        Post.like(db, id)
        return redirect("/post/"+image)
    if request.method == 'POST' and 'comment' in request.form:
        comment = request.form.get("comment")
        Post.addComment(db, comment, id)
        return redirect("/post/"+image)
    return render_template('post.html', id=id, postList=postList)


@app.route('/users', methods=["GET", "POST"])
def users():
    usersList = User.getusers()
    if request.method == 'POST':
        userToFollow = request.form.get('follow')
        print(userToFollow)
        username = str(session['_user_id'])
        User.follow(username, userToFollow)
        return redirect("/")
    return render_template('users.html', usersList=usersList)


@app.route('/profile/<username>', methods=["GET", "POST"])
def profile(username):
    imageList = User.imagesForUser(username)
    likes = Post.getAllLikes(username)
    followers = User.getUserFollowers(username)
    following = User.getUserFollowing(username)
    return render_template('profile.html', imageList=imageList, username=username, likes=likes, followers=followers, following=following)


app.config["IMAGE_UPLOADS"] = "static/images"
@app.route('/upload-image', methods=["GET", "POST"])
def postimage():
    if request.method == "POST":
        try:
            if request.files:
                image = request.files["image"]
                imageString = str(image)
                indexOne = imageString.index('\'')
                indexTwo = imageString.index('\'', indexOne+1)
                imageName = imageString[indexOne+1:indexTwo]
                indexOfDot = imageName.index('.')
                extensionName = imageName[indexOfDot+1::]
                if extensionName.lower() == "png" or extensionName.lower() == "jpg" or extensionName.lower() == "gif":
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                    print("Image saved")
                    return redirect("/caption/" + imageName)
                else:
                    return redirect("/upload-image")
        except:
            return redirect("/upload-image")
    return render_template("upload-image.html")


@app.route('/caption/<image>', methods=["GET", "POST"])
def postCaption(image):
    form = CaptionForm()
    if request.method == "POST":
        caption = form.caption.data
        username = str(session['_user_id'])
        Post.addPost(username, image, caption)
        return redirect("/post/"+image)
    return render_template('caption.html', form=form, image=image)


@app.route('/forgotPassword', methods=["GET","POST"])
def forgotPassword():
    form = EmailForm()
    if request.method == "POST":
        email = form.email.data
        print(email)
        link = "http://127.0.0.1:5000/resetPassword/"+email
        emailsend.send_email(email, link)
        return redirect("/")
    return render_template('forgotPassword.html', form=form)


@app.route('/resetPassword/<emailadress>', methods=["GET","POST"])
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
            email = emailadress
            # changePassword(email, password) implementation needed in database*************
            return redirect("/")
    return render_template('resetPassword.html', form=form, emailadress=emailadress)


if __name__ == '__main__':
    app.run()
    db.close()
