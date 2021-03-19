from posts import posts,getID,getListFromCSV,getAllLikes
import csv

def test_posts(): #This method check if the posts constructor is working properly
    instance = posts("Travis","picturepath","This is a test!")
    assert instance.likes == 0
    assert instance.user == "Travis"
    assert instance.imgpath == "picturepath"
    assert instance.comments == []

#Tests if the right picture ID is being returned by the method
def test_getInfo():
    postsList = getListFromCSV('data/posts.csv')
    ID = 1
    for posts in postsList:
        if posts[2] == "img(11).jpg":
            ID = posts[0]
    assert getID("img(11).jpg") == ID

#Tests if the getAllLikes method returns the proper number
def test_getAllLikes():
    postsList = getListFromCSV('data/posts.csv')
    user = 'Ablion73'
    totalLikes = 0
    for posts in postsList:
        if posts[1] == user:
            totalLikes = totalLikes+ int(posts[4])
    assert getAllLikes('Ablion73') == totalLikes