from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email, first_name, last_name, password, id=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.id = id

    def getUser(self):
        return (self.id, self.username, self.email, self.first_name, self.last_name, self.password)

    @staticmethod
    def _get_image(fname):
        """Convert digital data to binary format"""
        with open(fname, 'rb') as f:
            data = f.read()
        return data

    @staticmethod
    def getUsernames(db):
        """retrieve all user data"""
        cr = db.cursor(dictionary=True)
        cr.execute("SELECT username FROM user")
        usernames = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['username'], usernames))

    @staticmethod
    def getByID(db, id):
        """Search in db for row where id corresponds to given id"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM user WHERE id = '{id}'")
        try:
            fields = cr.fetchone()
            user = User(fields['username'], fields['email'], fields['first_name'], fields['last_name'], fields['password'], fields['id'])
        except KeyError:
            user = None
        cr.close()
        return user

    @staticmethod
    def getByUsername(db, username):
        """Search in db for row where username corresponds to given username"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM user WHERE username = '{username}'")
        try:
            fields = cr.fetchone()
            user = User(fields['username'], fields['email'], fields['first_name'], fields['last_name'], fields['password'], fields['id'])
        except KeyError:
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
    def getFollowers(db, user):
        """returns a list with all the followers of a specific user"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT user_id FROM follower WHERE following_id = '{user.id}'")
        users = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['user_id'], users))

    @staticmethod
    def getFollowing(db, user_id):
        """returns a list with all the followers of a specific user"""
        cr = db.cursor()
        cr.execute("SELECT * FROM follower WHERE id = '{}'".format(user_id))
        user = cr.fetchall()
        cr.close()
        return

    def getImages(db, user_id):
        """get the images a user has posted"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT image_id FROM post INNER JOIN image ON post.image_id = image.image WHERE user_id = {user_id}")
        images = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['image'].decode("utf-8")), images)

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

    # add users to db from csv
    # with open('data/users.csv', 'r') as f:
    #     for user in f.read().splitlines()[1:]:
    #         User.addUser(db, User(*user.split(',')))

    # add images to db from directory /static/user_images
    # cr = db.cursor()
    # for i in range(1, 258):
    #     data = (User._get_image(f'static/user_images/img({i}).jpg'),)
    #     cr.execute("INSERT INTO image (data) VALUES (%s)", data)
    #     db.commit()
    # cr.close()

    # retrieve all images from db, output to test directory
    # cr = db.cursor(dictionary=True)
    # cr.execute("SELECT data FROM image")
    # data = cr.fetchall()
    # cr.close()
    # images = list(map(lambda x: x['data'], data))
    # for i in range(len(images)):
    #     with open(f'test/img({i+1}).jpg', 'wb') as f:
    #         f.write(images[i])

    # add follower relationships to db
    # cr = db.cursor()
    # with open('data/followers.csv', 'r') as f:
    #     follower = f.read().splitlines()[1:]
    # for i in follower:
    #     users = i.split(',')
    #     user_id = User.getByUsername(db, users[0]).id
    #     # print(users[0], user_id)
    #     for following in users[1:]:
    #         following_id = User.getByUsername(db, following).id
    #         # print(user_id, following_id, sep=' -> ')
    #         cr.execute(f"INSERT INTO follower (user_id, following_id) VALUES ('{user_id}', '{following_id}')")
    #         db.commit()
    # cr.close()

    # print(User.getUsernames(db))
    # print(User.getByID(db, 1))
    # print(User.getByUsername(db, 'Ablion73'))
    # print(User.add())
    # print(User.isFollowable())
    # print(User.follow())
    # print(User.unfollow())
    print(User.getFollowers(db, 1))
    # print(User.getFollowing())

    # cr.execute("SELECT * FROM user")
    # print(cr.fetchall())
    db.close()
