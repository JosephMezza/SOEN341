from datetime import datetime

class Post():

    def __init__(self, user_id, image, time, caption=None, likes=0, id=None):
        self.id = id
        self.user_id = user_id
        self.image = image
        self.time = time
        self.caption = caption
        self.likes = likes
        try:
            self.comments = Comment.getPostComments(self.id)
        except (Exception, Exception) as e:
            self.comments = []

    def getPost(self):
        return (self.id, self.user_id, self.image, self.time, self.caption, self.likes)

    @staticmethod
    def getFullPost(db, post_id):
        """full information of the post, including image"""
        cr = db.cursor(dictionary=True)
        cr.execute(f"SELECT post.* FROM post INNER JOIN image ON post.id = '{post_id}' AND post.image_id = image.id")
        post = cr.fetchone()
        cr.close()
        return Post(post['user_id'], post['image'], post['time'], post['caption'], post['likes'], post['id'])

    @staticmethod
    def getID(db, image):
        """get ID from given image path"""
        cr = db.cursor(dictionary=True)
        cr.execute("SELECT id FROM post WHERE image_id = '{}'".format(image))
        image_id = cr.fetchone()
        cr.close()
        return image_id['id']

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

    @staticmethod
    def like(db, user, post):
        """user with user_id likes the post with the post_id"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes + 1 WHERE id = '{post.id}'") # Increments the likes
        cr.execute(f"INSERT INTO user_like post SET likes = likes + 1 WHERE id = '{post.id}'")
        cr.close()

    @staticmethod
    def unlike(db, user_id, post_id):
        """user with user_id unlikes the post with the post_id"""
        cr = db.cursor()
        cr.execute(f"UPDATE post SET likes = likes - 1 WHERE id = '{post_id}'") # Decrements the likes
        cr.close()

    @staticmethod
    def getTotalLikes(db, username):
        """returns all likes for a specific user"""
        cr = db.cursor(dictionary=True)
        cr.execute("SELECT likes FROM posts WHERE user = '{}'".format(username))
        total_likes = cr.fetchall()
        cr.close()
        return total_likes

    @staticmethod
    def getComments(db, post_id):
        """return the comments of a post in order of time posted"""
        cr = db.cursor()
        cr.execute("SELECT user_id, content FROM comments WHERE post_id = '{}'".format(post_id))
        comments = cr.fetchall()
        cr.close()
        return comments

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
    def add(db, post_id, comment):
        """add a comment to the specific post"""
        # MySQL datetime: YYYY-MM-DD hh:mm:ss
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cr = db.cursor()
        # cr.execute("UPDATE post SET comments = '{}' WHERE ID = '{}'".format(comment, post_id))
        db.commit()
        cr.close()


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
