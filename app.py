from re import I
from flask import Flask, session, redirect, render_template, flash, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, SignUpForm, CaptionForm, ResetPasswordForm, EmailForm
import bcrypt
import follower
import tornado.web
import tornado.ioloop
import os
from werkzeug.utils import secure_filename
import posts
import emailsend

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
    # print(session['username'])
    # eventually change to logged in user
    username = "Calasts53"
    imageList = []
    try:
        username = str(session['_user_id'])
        print(username)
        imageList = follower.getImagesToShow(username)
        imagedict = {imageList[index*2+1]: imageList[index*2] for index in len(imageList)/2-5}
        print(imagedict)
    except:
        print("An exception occurred")
        username = "Calasts53"
    print(username)
    

    return render_template('main.html', imageList=imageList) #, loggedIn=session['loggedIn']

# Test User:
# Calasts53
# eeG1fior0g
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
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
                return render_template('main.html')
        except:
            return redirect("/")
    return render_template('login.html', form=form, )#loggedIn=session['loggedIn']


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
    print(form.username)
    if form.validate_on_submit():
        # check first if user already exists
        user = find_user(form.username.data)
        if not user:
            # salt = bcrypt.gensalt()
            # password = bcrypt.hashpw(form.password.data.encode(), salt)
            follower.addUser(form.username.data, form.password.data, form.email.data, form.first_name.data, form.last_name.data)
            flash('Sign up successful.')
            return redirect('/login')
        else:
            flash('This username already exists')
    return render_template('signup.html', form=form)


@app.route('/post/<image>', methods=['GET', 'POST'])
def post(image):
    id= int(posts.getID(image))
    postList = posts.getInfo(id)
    if request.method == 'POST' and 'like' in request.form:
        posts.like(id)
        return redirect("/post/"+image)
    if request.method == 'POST' and 'comment' in request.form:
        comment = request.form.get("comment")
        print(comment)
        posts.addComment(comment, id)
        return redirect("/post/"+image)

        
        
    return render_template('post.html', id=id, postList = postList)


@app.route('/users' , methods=["GET","POST"])
def users():
    usersList = follower.getusers()
    if request.method == 'POST':
        userToFollow = request.form.get('follow')
        print(userToFollow)
        username = str(session['_user_id'])
        follower.follow(username, userToFollow)
        return redirect("/")
    return render_template('users.html', usersList = usersList)

@app.route('/profile/<username>' , methods=["GET","POST"])
def profile(username):
    print(username)
    imageList= follower.imagesForUser(username)
    print(imageList)
    likes = posts.getAllLikes(username)
    print(likes)
    followers = follower.getUserFollowers(username)
    following = follower.getUserFollowing(username)
    return render_template('profile.html', imageList = imageList, username = username, likes = likes, followers = followers, following = following)


app.config["IMAGE_UPLOADS"] = "static/images"



@app.route('/upload-image' , methods=["GET","POST"])
def postimage():
    if request.method == "POST":
        try:
            if request.files:
                image = request.files["image"]
                print(image)
                imageString = str(image)
                indexOne = imageString.index('\'')
                indexTwo = imageString.index('\'', indexOne+1)
                imageName = imageString[indexOne+1:indexTwo]
                print(imageName)
                indexOfDot = imageName.index('.')
                extensionName = imageName[indexOfDot+1::]
                print(extensionName)
                if extensionName.lower() == "png" or extensionName.lower() == "jpg" or extensionName.lower() == "gif":
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                    print("Image saved")
                    # return redirect(request.url)
                    return redirect("/caption/" + imageName)
                else:
                    return redirect("/upload-image")
        except: 
            return redirect("/upload-image")
    return render_template("upload-image.html")

@app.route('/caption/<image>', methods=["GET","POST"])
def postCaption(image):
    form = CaptionForm()
    if request.method == "POST":
        caption = form.caption.data
        if caption == "":
            return redirect("/caption/"+image)
        username = str(session['_user_id'])
        follower.addimage(username, image)
        posts.addPost(username, image, caption)
        return redirect("/post/"+image)
    return render_template('caption.html', form=form, image=image)


@app.route('/forgotPassword', methods=["GET","POST"])
def forgotPassword():
    form = EmailForm()
    if request.method == "POST":
        email = form.email.data
        print(email)
        link = "http://127.0.0.1:5000/resetPassword/"+email
        emailsend.sendemail(email, link)
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
            print(password)
            print(password2)
            # checks to see if password is good
            if password != password2:
                return redirect("/resetPassword/"+emailadress)

            email = emailadress
            print(email)
            # changePassword(email, password) implementation needed in database
            return redirect("/")
    return render_template('resetPassword.html', form=form, emailadress=emailadress)


if __name__ == '__main__':
    app.run()
