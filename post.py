from datetime import datetime

class Post():
    def __init__(self, user_id, image, time, caption=None, likes=0, id=None):
        self.id = id
        self.user_id = user_id
        self.image = image # base64
        self.time = time
        self.caption = caption
        self.likes = likes
        self.comments = Comment.get_comments(self)

    def get_post(self, dictionary=False):
        if dictionary:
            return dict(id=self.id, user_id=self.user_id, image=self.image, time=self.time, caption=self.caption, likes=self.likes)
        return (self.id, self.user_id, self.image, self.time, self.caption, self.likes)

    def get_full_post(self, db):
        """full information of the post, including image and comments, from db"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT post.* FROM post INNER JOIN image ON post.id = '{self.id}' AND post.image_id = image.id INNER JOIN ")
        post = cr.fetchone()
        cr.close()
        return Post(**post)

    @staticmethod
    def add(db, post, commit=True):
        """
        add a post to the post database
        TODO : This method isn't currently working, have to fix it
        """
        cr = db.cursor(dictionary=True)
        cr.execute("INSERT INTO post (user, image, caption, likes, time) VALUES ('{}', '{}', '{}', '{}', '{}')".format(*post.getPost()[1:]))
        # commit to database unless specified
        if commit:
            db.commit()
        cr.close()

    def __repr__(self):
        return 'Post({})'.format(self.id)


class Comment():
    def __init__(self, user_id, post_id, time, content, id=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.time = time
        self.content = content

    @staticmethod
    def get_comments(db, post):
        """returns a list with all the comments of a post"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT * FROM comment WHERE post_id = {post.id}")
        comments = cr.fetchall()
        cr.close()
        return list(map(lambda x: Comment(**x), comments))

    @staticmethod
    def add(db, post_id, comment):
        """add a comment to the specific post"""
        # MySQL datetime: YYYY-MM-DD hh:mm:ss
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cr = db.cursor()
        # cr.execute("UPDATE post SET comments = '{}' WHERE ID = '{}'".format(comment, post_id))
        db.commit()
        cr.close()


def get_image(fname):
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

    user_id = User.getByUsername(db, 0, dictionary=True)['id']
    # Sample post : Post(user_id, image, time)

    user_id = User.getUserByUsername('Ablion73', dictionary=True)['id']
    # image = GET_IMAGE

    # post = Post(user_id, image)
    Post.addPost(db, Post())

    print(Post.getInfo(db, 14))
    print(Post.getID(db, 'img(55).jpg'))
    print(Post.getAllLikes(db, 'Thithe'))
    db.close()
