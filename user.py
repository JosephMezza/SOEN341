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

    @staticmethod
    def _read_image(fname):
        with open(fname, 'rb') as f:
            image = f.read()
        return image

    @staticmethod
    def getUsernames(db):
        """retrieve all user data"""
        cr = db.cursor(dictionary=True)
        cr.execute("SELECT username FROM user")
        usernames = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['username'], usernames))

    @staticmethod
    def getByID(db, id, dictionary=False):
        """Search in db for row where id corresponds to given id"""
        cr = db.cursor(dictionary=dictionary)
        cr.execute(f"SELECT * FROM user WHERE id = '{id}'")
        try:
            user = User(*cr.fetchone())
        except TypeError:
            user = None
        cr.close()
        return user

    @staticmethod
    def getByUsername(db, username, dictionary=False):
        """Search in db for row where username corresponds to given username"""
        cr = db.cursor(dictionary=dictionary)
        cr.execute(f"SELECT * FROM user WHERE username = '{username}'")
        try:
            user = User(*cr.fetchone())
        except TypeError:
            user = None
        cr.close()
        return user

    @staticmethod
    def add(db, user):
        """Add a user to the database"""
        cr = db.cursor()
        fields = '(username, email, first_name, last_name, password)'
        add_user = ("INSERT INTO user {} VALUES ('{}', '{}', '{}', '{}', '{}')".format(fields, *user.getUser()[1:]))
        # Insert new user
        cr.execute(add_user)
        db.commit()
        cr.close()
        return

    @staticmethod
    def isFollowable(user_id, following_id):
        return user_id != following_id

    @staticmethod
    def follow(db, user_id, following_id):
        """follow another user"""
        # make sure you cannot follow yourself
        if not User.isFollowable(user_id, following_id):
            print('User cannot follow themselves')
            return

        cr = db.cursor()

        follow_user = (f"INSERT INTO follower (user_id, following_id) VALUES ({user_id}, {following_id})")
        cr.execute(follow_user)
        db.commit()
        cr.close()
        return

    @staticmethod
    def unfollow(db, user_id, following_id):
        """unfollow another user"""
        # make sure you cannot unfollow yourself
        if not User.isFollowable(user_id, following_id):
            print('User cannot unfollow themselves')
            return

        cr = db.cursor()

        unfollow_user = (f"DELETE FROM follower WHERE user_id = {user_id} AND following_id = {following_id}")
        cr.execute(unfollow_user)
        db.commit()
        cr.close()
        return

    @staticmethod
    def getFollowers(db, user_id):
        """returns a list with all the followers of a specific user"""
        cr = db.cursor()
        # cr.execute("SELECT * FROM follower WHERE id = '{}'".format(user_id))
        user = cr.fetchone()
        cr.close()
        return user[1:]

    @staticmethod
    def getFollowing(db, user_id):
        """returns a list with all the followers of a specific user"""
        cr = db.cursor()
        # cr.execute("SELECT * FROM follower WHERE id = '{}'".format(user_id))
        user = cr.fetchone()
        cr.close()
        return user[1:]

    def getImages(db, user_id):
        """get the images a user has posted"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT image_id FROM post INNER JOIN image ON post.image_id = image.image WHERE user_id = {user_id}")
        images = cr.fetchall()
        cr.close()
        return list(map(lambda x: b64encode(x['image']).decode("utf-8")), images)

    def __repr__(self):
        return 'User({})'.format(self.username)


if __name__ == '__main__':
    import mysql.connector

    db = mysql.connector.connect(
            host='192.168.1.53',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )

    # for loop to add users to db from csv
    # with open('data/users.csv', 'r') as f:
    #     for user in f.read().splitlines()[1:]:
    #         User.addUser(db, User(*user.split(',')))

    # for loop to add images to db from directory /static/user_images

    cr = db.cursor()
    for i in range(1, 258):
        image = User._read_image(f'static/user_images/img({i}).jpg')
        cr.execute(f"INSERT INTO image (data) VALUES ({image})")
    cr.close()

    # print(User.getUsernames(db))
    # print(User.getByID(db, 1))
    # print(User.getByUsername(db, 'Ablion73'))
    # print(User.add())
    # print(User.isFollowable())
    # print(User.follow())
    # print(User.unfollow())
    # print(User.getFollowers())
    # print(User.getFollowing())

    # cr = db.cursor()
    # cr.execute("SELECT * FROM user")
    # print(cr.fetchall())
    # cr.close()
    db.close()
