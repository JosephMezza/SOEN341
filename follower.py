import time
import csv
import random


def addUser(user):
    followerlist = []
    with open('data/followers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        followerlist = list(reader)
    # copy the csv information in a list


    for people in followerlist[0]:
        if people == user:
           return
    # Checks if it is a new user

    followerlist.append([user])
    followerlist[0].append(user)
    # inserting the new user inside the list
    
        
    with open('data/followers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(followerlist)
        #the list with the new user inserted



def follow(user, follower):

    followerlist = []
    with open('data/followers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        followerlist = list(reader)
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
    followerlist[followerIndex][userIndex] = 'X'
    #if a user follows another, a X is typed in their intersection in the list

    with open('data/followers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(followerlist)
        #the list with the new follower X  marked in it will be put back into the csv file


# returns a lsit with all the pictures they posted
def imagesForUser(user):
    imagelist = []
    with open('data/userimages.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        imagelist = list(reader)

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



# testof the methods
# addUser("Mikeyyy")
# follow("Drand1943","Milloon")
# follow("Drand1943","Drand1943")
# follow("Drand1943","wgerwgg")
# follow("sdfwergwghr","Drand1943")
# print(imagesForUser("Giarturner"))


# THIS CODE WILL RANDOMLY POPULATE AN IMAGE DATABASE
# imagelist = []
# with open('data/userimages.csv', newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         imagelist = list(reader)
# for users in imagelist:
#     for x in range(random.randint(1, 10)):
#         users.append("images\\img%20("+str(random.randint(1, 245))+").jpg")

# with open('data/userimages.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         writer.writerows(imagelist)