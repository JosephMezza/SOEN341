from flask_login import UserMixin
from base64 import b64encode


class User(UserMixin):
    _VALID_KEYS = {'id', 'username', 'email'}
    def __init__(self, username, email, first_name, last_name, password=None, id=None, commit_to_db=True):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.id = id
        self.commit_to_db = commit_to_db

    def get_user(self, dictionary=False, hide_password=False):
        user = dict(id=self.id, username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name, password=self.password)
        if hide_password:
            user['password'] = None
        if not dictionary:
            return tuple(val for val in user.values() if val != None)  # filter None types
        return user

    def get_followable(self, db):
        """get dict of all users where the ones which are followable are specified
        return dict : {User(): 'follow', User(): 'unfollow'}"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT username, id FROM user WHERE id != {self.id}")
        users = cr.fetchall()
        cr.execute(f"SELECT following_id FROM follower WHERE user_id = {self.id}")
        following = cr.fetchall()
        cr.close()
        following = set(map(lambda x: x['following_id'], following))
        return {user['username']: 'unfollow' if user['id'] in following else 'follow' for user in users}

    def is_followable(self, user):
        """compare user ids to check if user is followable"""
        return self != user

    def follow(self, db, user):
        """follow another user"""
        # make sure you cannot follow yourself
        if not self.is_followable(user):
            print('User cannot follow themselves')
            return

        cr = db.cursor()
        follow_user = (
            f"INSERT INTO follower (user_id, following_id) VALUES ({self.id}, {user.id})")
        cr.execute(follow_user)
        if self.commit_to_db:
            db.commit()
        cr.close()
        return

    def unfollow(self, db, user):
        """unfollow another user"""
        # make sure you cannot unfollow yourself
        if not self.is_followable(user):
            print('User cannot unfollow themselves')
            return

        cr = db.cursor()
        unfollow_user = (
            f"DELETE FROM follower WHERE user_id = {self.id} AND following_id = {user.id}")
        cr.execute(unfollow_user)
        if self.commit_to_db:
            db.commit()
        cr.close()
        return

    def get_followers(self, db):
        """returns a list with all the followers of a specific user"""
        cr = db.cursor(dictionary=True)
        cr.execute(
            f"SELECT user.* FROM user INNER JOIN follower ON user.id = follower.user_id AND follower.following_id = {self.id}")
        users = cr.fetchall()
        cr.close()
        return list(map(lambda x: User(**x), users))

    def get_following(self, db):
        """returns a list with all the users being followed a specific user"""
        cr = db.cursor(dictionary=True)
        cr.execute(
            f"SELECT user.* FROM user INNER JOIN follower ON user.id = follower.following_id AND follower.user_id = {self.id}")
        users = cr.fetchall()
        cr.close()
        return list(map(lambda x: User(**x), users))

    def get_post_images(self, db):
        """get post ids with base64 encoded string images as dict"""
        cr = db.cursor(dictionary=True)
        cr.execute(
            f"SELECT post.id, image.data FROM post INNER JOIN image ON post.image_id = image.id WHERE post.user_id = {self.id}")
        posts = cr.fetchall()
        cr.close()
        return {post['id']: b64encode(post['data']).decode('utf-8') for post in posts}

    def get_following_post_images(self, db):
        """get images to show on a user's homescreen as base64 encoded strings
        as a dict where post_id: image"""
        following = tuple(map(lambda x: x.id, self.get_following(db)))
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT post.id, image.data FROM post INNER JOIN image ON post.image_id = image.id WHERE post.user_id IN {following}")
        posts = cr.fetchall()
        cr.close()
        return {post['id']: b64encode(post['data']).decode('utf-8') for post in posts}

    def get_likes(self, db):
        """returns all likes for a user's posts"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT likes FROM post WHERE user_id = '{self.id}'")
        total_likes = cr.fetchall()
        cr.close()
        return sum(map(lambda x: int(x['likes']), total_likes))

    def change_password(self, db, new_password):
        """changes a user's password"""
        cr = db.cursor()
        cr.execute(f"UPDATE user SET password = {new_password} WHERE id = '{self.id}'")
        if self.commit_to_db:
            db.commit()
        cr.close()

    @staticmethod
    def get_usernames(db):
        """retrieve all user data"""
        cr = db.cursor(dictionary=True)
        cr.execute("SELECT username FROM user")
        usernames = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['username'], usernames))

    @staticmethod
    def get_from_db(db, key, value, hide_password=False, commit_to_db=True):
        """Search in db for row where id corresponds to given id"""
        if key not in User._VALID_KEYS:
            print('invalid key')
            return
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM user WHERE {key} = '{value}'")
        fields = cr.fetchone()
        cr.close()
        if hide_password:
            fields['password'] = None
        if commit_to_db:
            fields['commit_to_db'] = commit_to_db
        try:
            return User(**fields)
        except TypeError:
            return

    def add_to_db(self, db):
        """Add a user to the database"""
        user_data = self.get_user(dictionary=True)
        user_data.pop('id')  # ensure key assignment is handled by database
        cr = db.cursor()
        # Insert new user
        cr.execute(f"INSERT INTO user ({', '.join(user_data.keys())}) VALUES {tuple(user_data.values())}")
        if self.commit_to_db:
            db.commit()
        cr.close()

    def __eq__(self, user):
        """equate a user to another user by ids as they are unique"""
        return self.id == user.id

    def __hash__(self):
        """implemented in order to use users as keys in dict"""
        return hash(self.get_user(hide_password=True))

    def __repr__(self):
        """string representation of a user which displays username for shorthand"""
        return f'User({self.username})'


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
    #     data = (get_image(f'static/user_images/img({i}).jpg'),)
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

    # print(User.get_usernames(db))
    user = User.get_by_username(db, 'Ablion73')
    # print(user.get_user(dictionary=True, hide_password=True))
    user_by_id = User.get_by_id(db, 1)
    assert user == user_by_id, 'ids are different'
    # followable = user.get_followable(db)
    # print(user.id)
    # print(followable)
    # print(user.get_likes(db))
    print(user.get_following_post_images(db))
    # user = User('test', 'test.test@test.com', 'test', 'testy', 'password')
    # print(user.get_user(dictionary=True))
    # User.add_to_db(db, user)
    # user.follow(db, user_by_id)
    # user.unfollow(db, user_by_id)
    # print(user.get_followers(db))
    # print(user.get_following(db))
    # images = user.get_images(db)
    # print(images[0][:20])

    # cr.execute("SELECT * FROM user")
    # print(cr.fetchall())
    db.close()
