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

    def like(self, db, user):
        """post is liked by a user"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes + 1 WHERE id = '{self.id}'") # Increments the likes
        cr.execute(f"INSERT INTO user_like (user_id, post_id) VALUES ({user.id}, {self.id})")
        if self.commit_to_db:
            db.commit()
        cr.close()

    def unlike(self, db, user):
        """post is unliked by a user"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes - 1 WHERE id = '{self.id}'") # Decrements the likes
        cr.execute(f"DELETE FROM user_like WHERE user_id = {user.id} AND post_id = {self.id}")
        if self.commit_to_db:
            db.commit()
        cr.close()

    def get_user(self, db, hide_password=False, commit_to_db=True):
        """retrieve the user object for a post"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM user WHERE id = '{self.user_id}'")
        user = cr.fetchone()
        cr.close()
        if hide_password:
            user['password'] = None
        if commit_to_db:
            user['commit_to_db'] = commit_to_db
        try:
            return User(**user)
        except TypeError:
            return

    def get_user_likes(self, db):
        """get list of users who have liked post"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT user_id FROM user_like WHERE post_id = {self.id}")
        user_likes = tuple(map(lambda x: str(x['user_id']), cr.fetchall()))
        if not user_likes:
            return []
        cr.execute(f"SELECT username FROM user WHERE id IN ({', '.join(user_likes)})")
        users = cr.fetchall()
        cr.close()
        return list(map(lambda x: x['username'], users))

    def get_image(self, db):
        """retrieve the image data of a post as a base64 encoded string"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT data FROM image WHERE id = '{self.image_id}'")
        image = cr.fetchone()
        cr.close()
        return b64encode(image['data']).decode('utf-8')

    def add_to_db(self, db, image_path):
        """add post to db with image data provided in binary format"""
        image_data = get_binary(image_path)
        post_data = self.get_post(dictionary=True)
        post_data.pop('id')
        post_data.pop('image_id')
        cr = db.cursor(dictionary=True)
        cr.execute("INSERT INTO image (data) VALUES (%s)", (image_data,))
        cr.execute("SELECT id FROM image ORDER BY id DESC LIMIT 1;")
        post_data['image_id'] = cr.fetchone()['id']
        cr.execute(f"INSERT INTO post ({', '.join(post_data.keys())}) VALUES {tuple(post_data.values())}")
        cr.execute("SELECT id FROM post ORDER BY id DESC LIMIT 1;")
        post_id = cr.fetchone()['id']
        if self.commit_to_db:
            db.commit()
        cr.close()
        return post_id

    def change_caption(self, db, caption):
        """change the caption of a podt in the db"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET caption = '{caption}' WHERE id = '{self.id}'")
        if self.commit_to_db:
            db.commit()
        cr.close()

    @staticmethod
    def get_by_id(db, id, commit_to_db=True):
        """Search in db for row where id corresponds to given id"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM post WHERE id = {id}")
        fields = cr.fetchone()
        cr.close()
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

    def add_to_db(self, db):
        """add a comment to the database"""
        comment_data = self.get_comment(dictionary=True)
        comment_data.pop('id')
        cr = db.cursor()
        cr.execute(f"INSERT INTO comment ({', '.join(comment_data.keys())}) VALUES {tuple(comment_data.values())}")
        if self.commit_to_db:
            db.commit()
        cr.close()

    @staticmethod
    def get_post_comments(db, post):
        """returns a dict where username: Comment"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT comment.*, user.username FROM comment INNER JOIN user ON user.id = comment.user_id WHERE comment.post_id = {post.id}")
        comments = cr.fetchall()
        cr.close()
        if not comments:
            return dict()
        usernames = [comment.pop('username') for comment in comments]
        return dict(zip(usernames, map(lambda x: Comment(**x), comments)))

    def __repr__(self):
        return self.content


def get_binary(fname):
    """Convert image file to binary format"""
    with open(fname, 'rb') as f:
        data = f.read()
    return data


if __name__ == '__main__':
    import mysql.connector

    db = mysql.connector.connect(
            host='192.168.1.53',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )


    # set correct number of likes
    # cr = db.cursor(dictionary=True)
    # cr.execute("SELECT * FROM post")
    # posts = list(map(lambda x: Post(**x), cr.fetchall()))
    # for post in posts:
    #     try:
    #         likes = len(post.get_user_likes(db))
    #     except:
    #         continue
    #     cr.execute(f"UPDATE post SET likes = {likes} WHERE id = '{post.id}'")
    # cr.close()

    post = Post.get_by_id(db, 3)
    # print(post.get_post(dictionary=True))
    # image = get_binary('static/images/montreal.jpg')
    # post.add_to_db(db, image)
    print(Comment.get_post_comments(db, post))
    db.commit()
    db.close()
