import time
import csv
import random

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



def addUser(user):
    followerlist = getListFromCSV('data/followers.csv')
    # copy the csv information in a list


    for people in followerlist[0]:
        if people == user:
           return
    # Checks if it is a new user

    followerlist.append([user])
    followerlist[0].append(user)
    # inserting the new user inside the list
    
    setListCSV('data/followers.csv', followerlist)    
    #the list with the new user inserted



def follow(user, follower):

    followerlist = getListFromCSV('data/followers.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list

    if user == follower:
        return
        # testing to make sure you cannot follow yourself

    userExist = False
    followerExist = False
    for people in followerlist[0]:
        if people == user:
            userExist = True
        if people == follow:
            followerExist = True
    if not followerExist or not userExist:
        return
    # testing to make sure the user and followers are real
    
   

    userIndex = followerlist[0].index(user)
    followerIndex = followerlist[0].index(follower)
    followerlist[userIndex][followerIndex] = 'X'
    #if a user follows another, a X is typed in their intersection in the list

    setListCSV('data/followers.csv', followerlist)
    #the list with the new follower X  marked in it will be put back into the csv file


# returns a lsit with all the pictures they posted
def imagesForUser(user):
    imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file with the images and checks 

    userExist = False
    userIndex = 0
    for index, people in enumerate(imagelist):
        if people[0] == user:
            userExist = True
            userIndex = index
    if  not userExist:
        return 
    # testing to make sure the user is real and takes the users position

    # will return a list of all images the user has
    return imagelist[userIndex][1:]

# returns a list with all the followers of a specific user
def getUserFollowers(user):
    followerlist = getListFromCSV('data/followers.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list
    
    userExist = False
    for people in followerlist[0]:
        if people == user:
            userExist = True
    if  not userExist:
        return
    # testing to make sure the user and followers are real

    userIndex = followerlist[0].index(user)
    followers = []
    for x in range(len(followerlist[userIndex])):
        if followerlist[userIndex][x] == "X":
            followers.append(followerlist[x][0])
            # checks the user to see all the people they follow and store it in a list
    return followers


# returns a list with all images to be displayed for a user
def getImagesToShow(user):
    imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file with the images and checks 

    userExist = False
    for people in imagelist:
        if people[0] == user:
            userExist = True
    if  not userExist:
        return 
        # testing to make sure the user is real and takes the users position
    
    
    followerlist = getUserFollowers(user)
    picturesDisplay = []
    for follower in followerlist:
        picturesDisplay= picturesDisplay + imagesForUser(follower)
    return picturesDisplay
    


# testof the methods

# addUser("Mikeyyy")
# follow("Drand1943","Milloon")
# follow("Drand1943","Drand1943")
# follow("Drand1943","wgerwgg")
# follow("sdfwergwghr","Drand1943")
# print(imagesForUser("Giarturner"))
# print(getUserFollowers("Cagoo1938"))
# print(getImagesToShow("Cagoo1938"))
addUser("robadobbob")


# *************************************************************************DO NOT USE METHODS***************************************************************************

# THIS METHOD WILL RANDOMLY POPULATE AN IMAGE DATABASE, DO NOT USE
def populateImageDatabse():
    imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file where the images are stored and tracks the data inside a list

    for users in imagelist:
        for x in range(random.randint(1, 10)):
            users.append("images\\img%20("+str(random.randint(1, 245))+").jpg")
            # randomly assigns images to users

    with open('data/userimages.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(imagelist)
        # list with all users and pictures will be transposed in the csv


# this method will randomly populate the followers csv, do not overuse this method
def populateFollowerDatabase(): 
    followerlist = getListFromCSV('data/followers.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list

    for x in range(random.randint(1, 20000)):
        followerlist[random.randint(1, 1000)][random.randint(1, 1000)] = 'X'
        # randomly assigns followers to users.

    with open('data/followers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(followerlist)
        #the list with the new followers X  marked in it will be put back into the csv file



