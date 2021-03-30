from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, username, email, first_name, last_name, password, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def getUser(self):
        return (self.id, self.username, self.email, self.first_name, self.last_name, self.password)

    def __repr__(self):
        return 'User({})'.format(self.username)


def getUserNames(db):
    """retrieve all user data"""
    cr = db.cursor()
    cr.execute("SELECT username FROM user")
    usernames = cr.fetchall()
    cr.close()
    return usernames


def getUserByID(db, id, dictionary=False):
    """Search in db for row where id corresponds to given id"""
    cr = db.cursor(dictionary=dictionary)
    cr.execute("SELECT * FROM user WHERE id = '{}'".format(id))
    user = User(*cr.fetchone())
    cr.close()
    return user


def getUserByUsername(db, username, dictionary=False):
    """Search in db for row where username corresponds to given username"""
    cr = db.cursor(dictionary=dictionary)
    cr.execute("SELECT * FROM user WHERE username = '{}'".format(username))
    user = User(*cr.fetchone())
    cr.close()
    return user


def addUser(db, user):
    """Add a user to the database"""
    cr = db.cursor()
    fields = '(username, email, first_name, last_name, password)'
    add_user = ("INSERT INTO user {} VALUES ('{}', '{}', '{}', '{}', '{}')".format(fields, *user.getUser()[1:]))
    # Insert new user
    cr.execute(add_user)
    db.commit()
    cr.close()
    return


def isFollowable(user_id, following_id):
    return user_id != following_id


def follow(db, user_id, following_id):
    """follow another user"""
    # make sure you cannot follow yourself
    if not isFollowable(user_id, following_id):
        print('User cannot follow themselves')
        return

    cr = db.cursor()

    follow_user = ("INSERT INTO follower (user_id, following_id) VALUES ({}, {})".format(user_id, following_id))
    cr.execute(follow_user)
    db.commit()
    cr.close()
    return


def unfollow(db, user_id, following_id):
    """unfollow another user"""
    # make sure you cannot unfollow yourself
    if not isFollowable(user_id, following_id):
        print('User cannot unfollow themselves')
        return

    cr = db.cursor()

    unfollow_user = ("DELETE FROM follower WHERE user_id = {} AND following_id = {}".format(user_id, following_id))
    cr.execute(unfollow_user)
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


# TODO : adapt to MANY TO MANY relationship
def getUserFollowers(db, username):
    """returns a list with all the followers of a specific user"""
    cr = db.cursor()
    cr.execute("SELECT * FROM follower WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user[1:]


# TODO : adapt to MANY TO MANY relationship
def getUserFollowing(db, username):
    """returns a list with all users following a specific user"""
    cr = db.cursor()
    cr.execute("SELECT * FROM follower WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user[1:]


def getImagesToShow(db, username):
    """returns a list with all users following a specific user"""
    cr = db.cursor()
    cr.execute("SELECT * FROM image WHERE username = '{}'".format(username))
    user = cr.fetchone()
    cr.close()
    return user


# TODO : create ONE TO MANY relationship
def addImage(db, user, imageName):
    """add an image to a user's profile"""

    cr = db.cursor()

    # TODO : INSERT OPERATION
    add_image = ("INSERT INTO image".format(imageName))
    cr.execute(add_image)
    db.commit()
    cr.close()
    return


if __name__ == '__main__':
    import mysql.connector

    db = mysql.connector.connect(
            host='192.168.1.53',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )

    # for loop to add users to db from csv
    with open('data/users.csv', 'r') as f:
        for user in f.read().splitlines()[1:]:
            addUser(db, User(*user.split(',')))

    # print(getUserNames(db))
    # print(getUser(db, 'id', 5))
    # print(userImages(db, 'Ablion73'))
    # print(getUserFollowers(db, 'Ablion73'))

    cr = db.cursor()
    cr.execute("SELECT * FROM user")
    print(cr.fetchall())
    cr.close()
    db.close()
