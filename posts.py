import time
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
    def __init__(self, user, imgpath):
        self.likes = 0
        self.user = user
        self.imgpath = imgpath
        self.time = time.time()
        self.comments = []
        postsList = getListFromCSV('data/posts.csv')
        self.postID = len(postsList)-1



def addpost(user, imgpath):
    newPost = posts(user, imgpath)
    postsList = getListFromCSV('data/posts.csv')
    post = []
    post.append(newPost.postID)
    post.append(newPost.user)
    post.append(newPost.imgpath)
    post.append(newPost.likes)
    post.append(newPost.time)
    postsList.append(post)
    setListCSV('data/posts.csv', postsList)

def addComment(comment, postID):
    postsList = getListFromCSV('data/posts.csv')
    postsList[postID].append(comment)
    setListCSV('data/posts.csv', postsList)


addComment("wow so ugly!", 1)




