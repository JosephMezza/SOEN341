import time
from datetime import date
import mysql.connector

# def getListFromCSV(fileName):
#     dataList=[]
#     with open(fileName, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         dataList = list(reader)
#         return dataList


# def setListCSV(fileName, listToWrite):
#     with open(fileName, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         writer.writerows(listToWrite)


class Post():
    def __init__(self, user, imgpath, caption):
        self.likes = 0
        self.user = user
        self.imgpath = imgpath
        self.caption = caption
        today = date.today()
        self.time = today.strftime("%b-%d-%Y")
        self.comments = []
        # postsList = getListFromCSV('data/posts.csv') We shouldn't be needing this
        # self.postID = len(postsList)
        self.postID = 0

    def getPost(self):
        return (self.postID, self.user, self.imgpath, self.caption, self.likes, self.time)


def addPost(db, post, commit=True):
    """
    add a post to the post database
    TODO : This method isn't currently working, have to fix it
    """
    cr = db.cursor(dictionary=True)
    cr.execute("INSERT INTO posts (ID, user, image, caption, likes, time) VALUES ({})".format(*post.getPost()))
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

# TODO : Note to self - Fix addPost() & getALLlikes()

if __name__ == '__main__':
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

    print(getInfo(db, 14))
    print(getID(db, 'img(55).jpg'))
    print(getAllLikes(db, 'Thithe'))
