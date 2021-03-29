from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email, first_name, last_name, password=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def getUser(self):
        return (self.username, self.email, self.first_name, self.last_name, self.password)

    def __repr__(self):
        return 'User({})'.format(self.username)


def getAllUsers(db):
    """retrieve all user data"""
    cr = db.cursor(dictionary=True)
    cr.execute("SELECT * FROM users")
    users = cr.fetchall()
    cr.close()
    return users


def getUser(db, key, val):
    """Search in db for row where a value corresponds to a specific key (col)"""
    cr = db.cursor(dictionary=True)
    cr.execute("SELECT * FROM users WHERE {} = '{}'".format(key, val))
    user = cr.fetchall()
    cr.close()
    return user


def addUser(db, user, commit=True):
    """Add a user to the database"""
    cr = db.cursor()
    add_user = ("INSERT INTO users (Username, Email, First_Name, Last_Name, Password) VALUES ({})".format(
        *user.getUser()))
    # Insert new user
    cr.execute(add_user)
    # commit to database unless specified
    if commit:
        db.commit()

    cr.close()
    return


def follow(db, user, followed, commit=True):
    """follow another user"""
    # make sure you cannot follow yourself
    if user.username == followed.username:
        print('User cannot follow themselves')
        return

    cr = db.cursor()

    # TODO : INSERT OPERATION
    follow_user = ("INSERT INTO followers".format(user.username, followed.username))
    cr.execute(follow_user)
    # commit to database unless specified
    if commit:
        db.commit()

    cr.close()
    return


def userImages(db, username):
    """returns a list with all the pictures they posted"""
    cr = db.cursor()
    cr.execute("SELECT * FROM userImages WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user[1:]


def getUserFollowers(db, username):
    """returns a list with all the followers of a specific user"""
    cr = db.cursor()
    cr.execute("SELECT * FROM followers WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user[1:]


def getUserFollowing(db, username):
    """returns a list with all users following a specific user"""
    cr = db.cursor()
    cr.execute("SELECT * FROM followers WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user[1:]


def getImagesToShow(user):
    imagelist = getListFromCSV('data/userImages.csv')

    imageList = []
    for follower in getUserFollowers(user):
        imageList += imagesForUser(follower)
    return imageList


def addimage(user, imageName):
    imagelist = getListFromCSV('data/userimages.csv')

    for people in imagelist:
        if people[0] == user:
            people.append(imageName)

    setListCSV('data/userimages.csv', imagelist)


if __name__ == '__main__':
    import mysql.connector

    db = mysql.connector.connect(
            host='192.168.1.53',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )

    # cr = db.cursor()
    # cr.execute("SHOW COLUMNS FROM followers")
    # print(cr.fetchall())
    # cr.close()
    # db.close()

    # print(getAllUsers(db))
    # print(getUser(db, 'Username', 'Ablion73'))
    # print(userImages(db, 'Ablion73'))
    print(getUserFollowers(db, 'Ablion73'))
