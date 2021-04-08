from datetime import datetime
from base64 import b64encode


class Post():
    def __init__(self, user_id, image_id, time, caption=None, likes=0, id=None):
        self.id = id
        self.user_id = user_id
        self.image_id = image_id
        self.time = time
        self.caption = caption
        self.likes = likes

    def get_post(self, dictionary=False):
        if dictionary:
            return dict(id=self.id, user_id=self.user_id, image_id=self.image_id, time=self.time, caption=self.caption, likes=self.likes)
        return (self.id, self.user_id, self.image_id, self.time, self.caption, self.likes)

    def like(self, db, user):
        """post is liked by a user"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes + 1 WHERE id = '{self.id}'") # Increments the likes
        cr.execute(f"INSERT INTO user_like (user_id, post_id) VALUES ({user.id}, {self.id})")
        db.commit()
        cr.close()

    def unlike(self, db, user):
        """post is unliked by a user"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes - 1 WHERE id = '{self.id}'") # Decrements the likes
        cr.execute(f"DELETE FROM user_like WHERE user_id = {user.id} AND post_id = {self.id}")
        db.commit()
        cr.close()

    def get_image(self, db):
        """retrieve the image data of a post as a base64 encoded string"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT data FROM image WHERE id = '{self.image_id}'")
        image = cr.fetchone()
        cr.close()
        return b64encode(image['data']).decode('utf-8')

    def add_to_db(self, db, image):
        """add post to db with image data provided in binary format"""
        post_data = self.get_post(dictionary=True)
        post_data.pop('id')
        cr = db.cursor(dictionary=True)
        cr.execute("INSERT INTO image (data) VALUES (%s)", image)
        cr.execute("SELECT id FROM image ORDER BY id DESC LIMIT 1;")
        post_data['image_id'] = cr.fetchone()['id']
        cr.execute(f"INSERT INTO post ({', '.join(post_data.keys())}) VALUES {tuple(post_data.values())}")
        db.commit()
        cr.close()

    @staticmethod
    def get_by_id(db, id):
        """Search in db for row where id corresponds to given id"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM post WHERE id = {id}")
        try:
            fields = cr.fetchone()
            post = Post(**fields)
        except TypeError:
            post = None
        cr.close()
        return post

    def __repr__(self):
        return 'Post({})'.format(self.id)


class Comment():
    def __init__(self, user_id, post_id, time, content, id=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.time = time
        self.content = content

    def add_to_db(self, db):
        """add a comment to the specific post"""
        # MySQL datetime: YYYY-MM-DD hh:mm:ss
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cr = db.cursor()
        # cr.execute("UPDATE post SET comments = '{}' WHERE ID = '{}'".format(comment, post_id))
        db.commit()
        cr.close()

    @staticmethod
    def get_post_comments(db, post):
        """returns a list with all the comments of a post"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM comment WHERE post_id = {post.id}")
        comments = cr.fetchall()
        cr.close()
        return list(map(lambda x: Comment(**x), comments))


def get_binary(fname):
    """Convert digital data to binary format"""
    with open(fname, 'rb') as f:
        data = f.read()
    return data


if __name__ == '__main__':
    import mysql.connector
    from user import User

    db = mysql.connector.connect(
            host='192.168.1.53',
            user='root',
            passwd='Binstagram_341',
            database='binstagram'
            )

    # print all post data
    # cr = db.cursor()
    # cr.execute("SELECT * FROM posts")
    # info = cr.fetchall()
    # cr.close()
    # print(info)

    post = Post.get_by_id(db, 3)
    # print(post.get_post(dictionary=True))
    # image = get_binary('static/images/montreal.jpg')
    # post.add_to_db(db, image)

    db.close()
