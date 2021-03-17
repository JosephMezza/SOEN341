import csv
from follower import getListFromCSV, addUser,getusers,imagesForUser,getUserFollowers,getImagesToShow

def test_CSV():
    dataList = []
    with open("data/users.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dataList = list(reader)      
    assert getListFromCSV("data/users.csv") == dataList

# def test_AddUser():
#     followerlist = getListFromCSV('testData/testFollower.csv')
#     setListCSV('testData/testImages.csv', [])
#     followerlist.append(['JosephMezza'])
#     followerlist[0].append('JosephMezza')
#     followerlist[-1].append(',' * len(followerlist[0]))
#     setListCSV('testData/testFollower.csv', followerlist)
#     #the list with the new user inserted
#     userslist = getListFromCSV('testData/testUser.csv')
#     userslist.append(['JosephMezza', 'joseph@gmail.com', 'Joseph', 'Mezzacappa', '12345678A'])
#     setListCSV('testData/testUser.csv', userslist)
#     imagelist = getListFromCSV('testData/testImages.csv')
#     imagelist.append(['JosephMezza'])
#     setListCSV('testData/testImages.csv', imageList)

#     assert 

def test_getUsers():
    followerlist = getListFromCSV('data/followers.csv')
    assert getusers() == followerlist[0][1:]

def test_imagesForUser():
    imagelist = getListFromCSV('data/userimages.csv')
    userIndex = -1
    for index, people in enumerate(imagelist):
        if people[0] == 'Ablion73':
            userIndex = index
    if not userIndex:
        return
    assert imagesForUser('Ablion73') == imagelist[userIndex][1:]

def test_getUserFollowers():
    followerlist = getListFromCSV('data/followers.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list  
    userExist = False
    for people in followerlist[0]:
        if people == 'Ablion73':
            userExist = True
    if  not userExist:
        return
    # testing to make sure the user and followers are real

    userIndex = followerlist[0].index('Ablion73')
    followers = []
    for x in range(len(followerlist[userIndex])):
        if followerlist[userIndex][x] == "X":
            followers.append(followerlist[x][0])
            # checks the user to see all the people they follow and store it in a list
    assert getUserFollowers('Ablion73') == followers

def test_getImagesToShow():
    user = 'Ablion73'
    username = user
    imagelist = getListFromCSV('data/userimages.csv')
    imageList = []
    for follower in getUserFollowers(user):
        print(imagesForUser(follower))
        imageList += imagesForUser(follower)
    assert getImagesToShow('Ablion73') == imageList