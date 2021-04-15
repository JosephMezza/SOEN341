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

    def get_followable(self, data_base):
        """get dict of all users where the ones which are followable are specified
        return dict : {User(): 'follow', User(): 'unfollow'}"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT username, id FROM user WHERE id != {self.id}")
        users = cursor.fetchall()
        cursor.execute(f"SELECT following_id FROM follower WHERE user_id = {self.id}")
        following = cursor.fetchall()
        cursor.close()
        following = set(map(lambda x: x['following_id'], following))
        return {user['username']: 'unfollow' if user['id'] in following else 'follow' for user in users}

    def is_followable(self, user):
        """compare user ids to check if user is followable"""
        return self != user

    def follow(self, data_base, user):
        """follow another user"""
        # make sure you cannot follow yourself
        if not self.is_followable(user):
            print('User cannot follow themselves')
            return

        cursor = data_base.cursor()
        follow_user = (
            f"INSERT INTO follower (user_id, following_id) VALUES ({self.id}, {user.id})")
        cursor.execute(follow_user)
        if self.commit_to_db:
            data_base.commit()
        cursor.close()
        return

    def unfollow(self, data_base, user):
        """unfollow another user"""
        # make sure you cannot unfollow yourself
        if not self.is_followable(user):
            print('User cannot unfollow themselves')
            return

        cursor = data_base.cursor()
        unfollow_user = (
            f"DELETE FROM follower WHERE user_id = {self.id} AND following_id = {user.id}")
        cursor.execute(unfollow_user)
        if self.commit_to_db:
            data_base.commit()
        cursor.close()
        return

    def get_followers(self, data_base):
        """returns a list with all the followers of a specific user"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(
            f"SELECT user.* FROM user INNER JOIN follower ON user.id = follower.user_id AND follower.following_id = {self.id}")
        users = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: User(**x), users))

    def get_following(self, data_base):
        """returns a list with all the users being followed a specific user"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(
            f"SELECT user.* FROM user INNER JOIN follower ON user.id = follower.following_id AND follower.user_id = {self.id}")
        users = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: User(**x), users))

    def get_post_images(self, data_base):
        """get post ids with base64 encoded string images as dict"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(
            f"SELECT post.id, image.data FROM post INNER JOIN image ON post.image_id = image.id WHERE post.user_id = {self.id}")
        posts = cursor.fetchall()
        cursor.close()
        return {post['id']: b64encode(post['data']).decode('utf-8') for post in posts}

    def get_following_post_images(self, data_base):
        """get images to show on a user's homescreen as base64 encoded strings
        as a dict where post_id: image"""
        following = tuple(map(lambda x: x.id, self.get_following(data_base)))
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT post.id, image.data FROM post INNER JOIN image ON post.image_id = image.id WHERE post.user_id IN {following}")
        posts = cursor.fetchall()
        cursor.close()
        return {post['id']: b64encode(post['data']).decode('utf-8') for post in posts}

    def get_likes(self, data_base):
        """returns all likes for a user's posts"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT likes FROM post WHERE user_id = '{self.id}'")
        total_likes = cursor.fetchall()
        cursor.close()
        return sum(map(lambda x: int(x['likes']), total_likes))

    def change_password(self, data_base, new_password):
        """changes a user's password"""
        cursor = data_base.cursor()
        cursor.execute(f"UPDATE user SET password = '{new_password.decode()}' WHERE id = {self.id}")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

    @staticmethod
    def get_usernames(data_base):
        """retrieve all user data"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute("SELECT username FROM user")
        usernames = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: x['username'], usernames))

    @staticmethod
    def get_from_db(data_base, key, value, hide_password=False, commit_to_db=True):
        """Search in db for row where id corresponds to given id"""
        if key not in User._VALID_KEYS:
            print('invalid key')
            return
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user WHERE {key} = '{value}'")
        fields = cursor.fetchone()
        cursor.close()
        if not fields:
            return
        if hide_password:
            fields['password'] = None
        if commit_to_db:
            fields['commit_to_db'] = commit_to_db
        try:
            return User(**fields)
        except TypeError:
            return

    def add_to_db(self, data_base):
        """Add a user to the database"""
        user_data = self.get_user(dictionary=True)
        user_data.pop('id')  # ensure key assignment is handled by database
        cursor = data_base.cursor()
        # Insert new user
        cursor.execute(f"INSERT INTO user ({', '.join(user_data.keys())}) VALUES {tuple(user_data.values())}")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

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

    data_base = mysql.connector.connect(
        host='192.168.1.53',
        user='root',
        passwd='Binstagram_341',
        database='binstagram'
    )

    # add users to db from csv
    # with open('data/users.csv', 'r') as f_name:
    #     for user in f_name.read().splitlines()[1:]:
    #         User.addUser(data_base, User(*user.split(',')))

    # add images to db from directory /static/user_images
    # cursor = data_base.cursor()
    # for i in range(1, 258):
    #     data = (get_image(f'static/user_images/img({i}).jpg'),)
    #     cursor.execute("INSERT INTO image (data) VALUES (%s)", data)
    #     data_base.commit()
    # cursor.close()

    # retrieve all images from data_base, output to test directory
    # cursor = data_base.cursor(dictionary=True)
    # cursor.execute("SELECT data FROM image")
    # data = cursor.fetchall()
    # cursor.close()
    # images = list(map(lambda x: x['data'], data))
    # for i in range(len(images)):
    #     with open(f'test/img({i+1}).jpg', 'wb') as f_name:
    #         f.write(images[i])

    # add follower relationships to db
    # cursor = data_base.cursor()
    # with open('data/followers.csv', 'r') as f_name:
    #     follower = f_name.read().splitlines()[1:]
    # for i in follower:
    #     users = i.split(',')
    #     user_id = User.getByUsername(data_base, users[0]).id
    #     # print(users[0], user_id)
    #     for following in users[1:]:
    #         following_id = User.getByUsername(data_base, following).id
    #         # print(user_id, following_id, sep=' -> ')
    #         cursor.execute(f"INSERT INTO follower (user_id, following_id) VALUES ('{user_id}', '{following_id}')")
    #         data_base.commit()
    # cursor.close()

    # print(User.get_usernames(data_base))
    user = User.get_from_db(data_base, 'username', 'Ablion73')
    # print(user.get_user(dictionary=True, hide_password=True))
    user_by_id = User.get_from_db(data_base, 'id', 1)
    assert user == user_by_id, 'ids are different'
    # followable = user.get_followable(data_base)
    # print(user.id)
    # print(followable)
    # print(user.get_likes(data_base))
    # print(user.get_following_post_images(data_base))
    # user = User('test', 'test.test@test.com', 'test', 'testy', 'password')
    # print(user.get_user(dictionary=True))
    # User.add_to_db(data_base, user)
    # user.follow(data_base, user_by_id)
    # user.unfollow(data_base, user_by_id)
    # print(user.get_followers(data_base))
    # print(user.get_following(data_base))
    # images = user.get_images(data_base)
    # print(images[0][:20])

    # cursor.execute("SELECT * FROM user")
    # print(cursor.fetchall())
    data_base.close()
