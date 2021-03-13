import time
from datetime import date
import csv
def getListFromCSV(fileName):
    dataList=[]
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        dataList = list(reader)
        return dataList

def setListCSV(fileName, listToWrite):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(listToWrite)



class posts:
    def __init__(self, user, imgpath, caption):
        self.likes = 0
        self.user = user
        self.imgpath = imgpath
        self.caption = caption
        today = date.today() 
        self.time = today.strftime("%b-%d-%Y")
        self.comments = []
        postsList = getListFromCSV('data/posts.csv')
        self.postID = len(postsList)-1



def addPost(user, imgpath, caption):
    newPost = posts(user, imgpath, caption)
    postsList = getListFromCSV('data/posts.csv')
    post = []
    post.append(newPost.postID)
    post.append(newPost.user)
    post.append(newPost.imgpath)
    post.append(newPost.caption)
    post.append(newPost.likes)
    post.append(newPost.time)
    postsList.append(post)
    setListCSV('data/posts.csv', postsList)

def addComment(comment, postID):
    postsList = getListFromCSV('data/posts.csv')
    postsList[postID+1].append(comment)
    setListCSV('data/posts.csv', postsList)

def like(postID):
    postsList = getListFromCSV('data/posts.csv')
    likes = int(postsList[postID+1][4])
    likes=likes+1
    postsList[postID+1][4]= likes
    setListCSV('data/posts.csv', postsList)

def getInfo(ID):
    postsList = getListFromCSV('data/posts.csv')
    return postsList[ID+1]


<<<<<<< HEAD
# addPost("Poters", "img(3).jpg", "LOOK AT lolol")
=======
#addPost("Poters", "img(3).jpg", "LOOK AT lolol")
>>>>>>> 7fdd49687622ce4bffde6ef368526c2e00b71c0c
# addComment("OMG MARY ME plssssss!!!!", 1)
# like(1)
# print(getInfo(0))