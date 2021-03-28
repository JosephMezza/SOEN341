import time
from datetime import date
import mysql.connector

""" def getListFromCSV(fileName):
    dataList=[]
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        dataList = list(reader)
        return dataList  

def setListCSV(fileName, listToWrite):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(listToWrite)"""

#I don't think we'll be needing this

db = mysql.connector.connect(
    host="184.144.173.26",
    user="root",
    passwd="Binstagram_341",
    database="binstagram"
)

class posts:
    def __init__(self, user, imgpath, caption):
        self.likes = 0
        self.user = user
        self.imgpath = imgpath
        self.caption = caption
        today = date.today() 
        self.time = today.strftime("%b-%d-%Y")
        self.comments = []
        # postsList = getListFromCSV('data/posts.csv') We shouldn't be needing this 
        self.postID = len(postsList) 


# this method will add a post to the post dataabse
def addPost(user, imgpath, caption):  #This method isn't currently working, have to fix it
    cr = db.cursor() 
    cr.execute("INSERT INTO posts (ID, user, image, caption, likes, time) VALUES (%s,%s,%s,%s,%s,%s)", (postID, user, imgpath, caption, likes, time)) #will postID, likes & time be generated?
    db.commit() #commits the changes to the database

# adds a comment to the specific post
def addComment(comment, postID): """TO DO: Lengthen the number of characters for COMMENTS"""
    cr.execute("UPDATE posts SET comments = '{}' WHERE ID = '{}'".format(comment, postID)) 
    db.commit()

# likes the post with the ID
def like(ID):
    cr.execute ("UPDATE posts SET likes = likes + 1 WHERE ID = '{}'".format(ID)) #Increments the likes
    db.commit()

# returns the full information of the post
def getInfo(ID):
    cr.execute("SELECT*FROM posts WHERE ID = '{}'".format(ID)) 
    for i in cr:
        print(i)

# gets ID when passed an image path
def getID(image):
    cr.execute("SELECT ID FROM posts WHERE image = '{}'".format(image))
    for i in cr:
        print(i)

#returns all likes for a specific user
def getAllLikes(user):
    a = []
    cr.execute("SELECT likes FROM posts WHERE user = 'Ablion73'")
    for i in cr:
    a.append(i)
    """ TO DO: Have to transform array elements to INT !!! """
    totalLikes = sum(a)
    





#Note to self: Fix addPost() & getALLlikes()