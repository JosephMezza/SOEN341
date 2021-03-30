from datetime import date

class Post():
    def __init__(self, user_id, image, time, caption=None, likes=0, id=None):
        self.id = id
        self.user_id = user_id
        self.image = image
        # today = date.today().strftime("%b-%d-%Y")
        self.time = time
        self.caption = caption
        self.likes = likes
        try:
            self.comments = getComments(self.id)
        except (Exception, Exception) as e:
            print(e)
            self.comments = []

    def getPost(self):
        return (self.id, self.user_id, self.image, self.time, self.caption, self.likes)

    def __repr__(self):
        return 'Post({})'.format(self.id)


class Comment():
    def __init__(self, user_id, post_id, time, content, id=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        # today = date.today().strftime("%b-%d-%Y")
        self.time = time
        self.content = content


def addPost(db, post, commit=True):
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


def addComment(db, comment, postID, commit=True):
    """add a comment to the specific post"""
    cr = db.cursor(dictionary=True)
    cr.execute("UPDATE posts SET comments = '{}' WHERE ID = '{}'".format(comment, postID))
    # commit to database unless specified
    if commit:
        db.commit()
    cr.close()


def like(db, ID, commit=True):
    """likes the post with the ID"""
    cr = db.cursor(dictionary=True)
    cr.execute("UPDATE posts SET likes = likes + 1 WHERE ID = '{}'".format(ID)) #Increments the likes
    # commit to database unless specified
    if commit:
        db.commit()
    cr.close()


def unlike(db, ID, commit=True):
    """likes the post with the ID"""
    cr = db.cursor(dictionary=True)
    cr.execute("UPDATE posts SET likes = likes - 1 WHERE ID = '{}'".format(ID)) #Decrements the likes
    # commit to database unless specified
    if commit:
        db.commit()
    cr.close()


def getInfo(db, ID):
    """full information of the post"""
    cr = db.cursor(dictionary=True)
    cr.execute("SELECT * FROM posts WHERE ID = '{}'".format(ID))
    info = cr.fetchone()
    cr.close()
    return info


def getID(db, image):
    """get ID from given image path"""
    cr = db.cursor()
    cr.execute("SELECT ID FROM posts WHERE image = '{}'".format(image))
    image_id = cr.fetchone()
    cr.close()
    return int(image_id[0])


def getAllLikes(db, username):
    """returns all likes for a specific user"""
    cr = db.cursor()
    cr.execute("SELECT likes FROM posts WHERE user = '{}'".format(username))
    total_likes = sum(map(lambda x: int(x[0]), cr.fetchall()))
    cr.close()
    return total_likes


def getComments(db, post_id):
    """return the comments of a post in order of time posted"""
    cr = db.cursor()
    cr.execute("SELECT user_id, content FROM comments WHERE post_id = '{}'".format(post_id))
    comments = cr.fetchall()
    cr.close()
    return comments


if __name__ == '__main__':
    import mysql.connector
    import user

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
    # sample post : (14, 'Thithe', 'img(14).jpg', 'Random caption14', 0, datetime.datetime(2021, 3, 14, 0, 0), None)

    user_id = user.getUserByUsername('Ablion73', dictionary=True)['id']
    # image = GET_IMAGE

    # post = Post(user_id, image)
    addPost(db, Post())

    print(getInfo(db, 14))
    print(getID(db, 'img(55).jpg'))
    print(getAllLikes(db, 'Thithe'))
    db.close()
