from user import User
from base64 import b64encode


class Post():
    def __init__(self, user_id, time, caption='', image_id=None, likes=0, id=None, commit_to_db=True):
        self.id = id
        self.user_id = user_id
        self.time = time
        self.caption = caption
        self.image_id = image_id
        self.likes = likes
        self.commit_to_db = commit_to_db

    def get_post(self, dictionary=False):
        if dictionary:
            return dict(id=self.id, user_id=self.user_id, image_id=self.image_id, time=self.time, caption=self.caption, likes=self.likes)
        return (self.id, self.user_id, self.image_id, self.time, self.caption, self.likes)

    def like(self, data_base, user):
        """post is liked by a user"""
        cursor = data_base.cursor()
        cursor.execute(f"UPDATE post SET likes = likes + 1 WHERE id = '{self.id}'") # Increments the likes
        cursor.execute(f"INSERT INTO user_like (user_id, post_id) VALUES ({user.id}, {self.id})")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

    def unlike(self, data_base, user):
        """post is unliked by a user"""
        cursor = data_base.cursor()
        cursor.execute(f"UPDATE post SET likes = likes - 1 WHERE id = '{self.id}'") # Decrements the likes
        cursor.execute(f"DELETE FROM user_like WHERE user_id = {user.id} AND post_id = {self.id}")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

    def get_user(self, data_base, hide_password=False, commit_to_db=True):
        """retrieve the user object for a post"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user WHERE id = '{self.user_id}'")
        user = cursor.fetchone()
        cursor.close()
        if hide_password:
            user['password'] = None
        if commit_to_db:
            user['commit_to_db'] = commit_to_db
        try:
            return User(**user)
        except TypeError:
            return

    def get_user_likes(self, data_base):
        """get list of users who have liked post"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT user_id FROM user_like WHERE post_id = {self.id}")
        user_likes = tuple(map(lambda x: str(x['user_id']), cursor.fetchall()))
        if not user_likes:
            return []
        cursor.execute(f"SELECT username FROM user WHERE id IN ({', '.join(user_likes)})")
        users = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: x['username'], users))

    def get_image(self, data_base):
        """retrieve the image data of a post as a base64 encoded string"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT data FROM image WHERE id = '{self.image_id}'")
        image = cursor.fetchone()
        cursor.close()
        return b64encode(image['data']).decode('utf-8')

    def add_to_db(self, data_base, image_path):
        """add post to db with image data provided in binary format"""
        image_data = get_binary(image_path)
        post_data = self.get_post(dictionary=True)
        post_data.pop('id')
        post_data.pop('image_id')
        cursor = data_base.cursor(dictionary=True)
        cursor.execute("INSERT INTO image (data) VALUES (%s)", (image_data,))
        cursor.execute("SELECT id FROM image ORDER BY id DESC LIMIT 1;")
        post_data['image_id'] = cursor.fetchone()['id']
        cursor.execute(f"INSERT INTO post ({', '.join(post_data.keys())}) VALUES {tuple(post_data.values())}")
        cursor.execute("SELECT id FROM post ORDER BY id DESC LIMIT 1;")
        post_id = cursor.fetchone()['id']
        if self.commit_to_db:
            data_base.commit()
        cursor.close()
        return post_id

    def change_caption(self, data_base, caption):
        """change the caption of a podt in the db"""
        cursor = data_base.cursor()
        cursor.execute(f"UPDATE post SET caption = '{caption}' WHERE id = '{self.id}'")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

    @staticmethod
    def get_by_id(data_base, id, commit_to_db=True):
        """Search in db for row where id corresponds to given id"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM post WHERE id = {id}")
        fields = cursor.fetchone()
        cursor.close()
        if commit_to_db:
            fields['commit_to_db'] = commit_to_db
        try:
            return Post(**fields)
        except TypeError:
            return

    def __repr__(self):
        return 'Post({})'.format(self.id)


class Comment():
    def __init__(self, user_id, post_id, time, content, id=None, commit_to_db=True):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.time = time
        self.content = content
        self.commit_to_db = commit_to_db

    def get_comment(self, dictionary=False):
        if dictionary:
            return dict(id=self.id, user_id=self.user_id, post_id=self.post_id, time=self.time, content=self.content)
        return (self.id, self.user_id, self.post_id, self.time, self.content)

    def add_to_db(self, data_base):
        """add a comment to the database"""
        comment_data = self.get_comment(dictionary=True)
        comment_data.pop('id')
        cursor = data_base.cursor()
        cursor.execute(f"INSERT INTO comment ({', '.join(comment_data.keys())}) VALUES {tuple(comment_data.values())}")
        if self.commit_to_db:
            data_base.commit()
        cursor.close()

    @staticmethod
    def get_post_comments(data_base, post):
        """returns a dict where username: Comment"""
        cursor = data_base.cursor(dictionary=True)
        cursor.execute(f"SELECT comment.*, user.username FROM comment INNER JOIN user ON user.id = comment.user_id WHERE comment.post_id = {post.id}")
        comments = cursor.fetchall()
        cursor.close()
        if not comments:
            return [()]
        usernames = [comment.pop('username') for comment in comments]
        return list(zip(usernames, map(lambda x: Comment(**x), comments)))

    def __repr__(self):
        return self.content


def get_binary(fname):
    """Convert image file to binary format"""
    with open(fname, 'rb+') as f_name:
        data = f_name.read()
    return data


if __name__ == '__main__':
    import mysql.connector

    db = mysql.connector.connect(
            host='184.144.173.26',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )


    # set correct number of likes
    # cursor = data_base.cursor(dictionary=True)
    # cursor.execute("SELECT * FROM post")
    # posts = list(map(lambda x: Post(**x), cursor.fetchall()))
    # for post in posts:
    #     try:
    #         likes = len(post.get_user_likes(data_base))
    #     except:
    #         continue
    #     cursor.execute(f"UPDATE post SET likes = {likes} WHERE id = '{post.id}'")
    # cursor.close()

    post = Post.get_by_id(data_base, 162)
    # print(post.get_post(dictionary=True))
    # image = get_binary('static/images/montreal.jpg')
    # post.add_to_db(data_base, image)
    print(Comment.get_post_comments(data_base, post))
    data_base.commit()
    data_base.close()
