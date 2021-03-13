import csv
import posts
def getListFromCSV(fileName):
    dataList = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dataList = list(reader)
    return dataList


def setListCSV(fileName, listToWrite):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(listToWrite)


def getusers():
    followerlist = getListFromCSV('data/followers2.csv')
    newfollowerslist=[]
    for people in followerlist:
        newfollowerslist.append(people[0])
    return newfollowerslist


def addUser(user, password, email, firstName, lastName):
    followerlist = getListFromCSV('data/followers2.csv')

    # copy the csv information in a list

    # for people in followerlist[0]:
    #     if people == user:
    #        return
    # Checks if it is a new user

    followerlist.append([user])
    # inserting the new user inside the list

    setListCSV('data/followers2.csv', followerlist)
    #the list with the new user inserted

    userslist = getListFromCSV('data/users.csv')
    userslist.append([user, email, firstName, lastName, password])
    setListCSV('data/users.csv', userslist)

    imagelist = getListFromCSV('data/userImages.csv')
    imagelist.append([user])
    setListCSV('data/userImages.csv', imagelist)


def follow(user, follower):
    followerlist = getListFromCSV('data/followers2.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list

    if user == follower:
        return
        # testing to make sure you cannot follow yourself

    for people in followerlist:
        if people[0] == user:
            people.append(follower)

    # userExist = False
    # followerExist = False
    # for people in followerlist[0]:
    #     if people == user:
    #         userExist = True
    #     if people == follow:
    #         followerExist = True
    # if not followerExist or not userExist:
    #     print("big problem")
    #     return
    # testing to make sure the user and followers are real

    # userIndex = followerlist[0].index(user)
    # followerIndex = followerlist[0].index(follower)
    # followerlist[userIndex][followerIndex] = 'X'

    
    #if a user follows another, a X is typed in their intersection in the list

    setListCSV('data/followers2.csv', followerlist)
    #the list with the new follower X  marked in it will be put back into the csv file


# returns a lsit with all the pictures they posted
def imagesForUser(user):
    imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file with the images and checks

    userIndex = -1
    for index, people in enumerate(imagelist):
        if people[0] == user:
            userIndex = index
    if not userIndex:
        return
    # testing to make sure the user is real and takes the users position

    # will return a list of all images the user has
    return imagelist[userIndex][1:]


# returns a list with all the followers of a specific user
def getUserFollowers(user):
    followerlist = getListFromCSV('data/followers2.csv')
        # opens the csv file where the followers are stored and tracks the data inside a list
    if followerlist[0][0][3:]== user:
        return followerlist[0][1:]

    userExist = False
    for people in followerlist:
        if people[0] == user:
            return people[1:]
    if  not userExist:
        return
    # testing to make sure the user and followers are real

    # userIndex = followerlist[0].index(user)
    # followers = []
    # for x in range(len(followerlist[userIndex])):
    #     if followerlist[userIndex][x] == "X":
    #         followers.append(followerlist[x][0])
    #         # checks the user to see all the people they follow and store it in a list
    # return followers


# returns a list with all images to be displayed for a user
def getImagesToShow(user):
    username = user
    imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file with the images and checks

    # userExist = False
    # for people in imagelist:
    #     if people[0] == user:
    #         userExist = True
    # if  not userExist:
    #     return
        # testing to make sure the user is real and takes the users position

    imageList = []
    for follower in getUserFollowers(user):
        print(imagesForUser(follower))
        imageList += imagesForUser(follower)
    return imageList


def addimage(user, imageName):
    imagelist = getListFromCSV('data/userimages.csv') 

    for people in imagelist:
        if people[0] == user:
            people.append(imageName)


    setListCSV('data/userimages.csv', imagelist)


if __name__ == '__main__':
    import random

    def populateImageDatabse():
        """THIS METHOD WILL RANDOMLY POPULATE AN IMAGE DATABASE, DO NOT USE"""
        imagelist = getListFromCSV('data/userimages.csv')
        # opens the csv file where the images are stored and tracks the data inside a list
        id =0 
        for users in imagelist:
            for x in range(5):
                image = "img("+str(random.randint(1, 245))+").jpg"
                users.append(image)
                users.append(id)
                posts.addPost(users[0], image, "Random caption"+str(id))
                id = id+1
                # randomly assigns images to users

        with open('data/userimages.csv', 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(imagelist)
            # list with all users and pictures will be transposed in the csv


    def populateFollowerDatabase():
        """this method will randomly populate the followers csv, do not overuse this method"""
        followerlist = getListFromCSV('data/followers2.csv')
            # opens the csv file where the followers are stored and tracks the data inside a list
        newfollowerslist=[]
        for users in followerlist:
            users= [users[0]]
            for x in range(10):
                users.append(followerlist[random.randint(1, 1002)][0])
            newfollowerslist.append(users)

        # for x in range(random.randint(1, 20000)):
        #     followerlist[random.randint(1, 1000)][random.randint(1, 1000)] = 'X'
            # randomly assigns followers to users

        with open('data/followers2.csv', 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(newfollowerslist)
            # the list with the new followers X marked in it will be put back into the csv file


    def hash_passwords():
        with open('data/users.csv', 'r') as f:
            pass

    # addUser("Mikeyyy")
    # follow("Drand1943","Ablion73")
    # follow("Drand1943","wgerwgg")
    # follow("Drand1943","wgerwgg")
    # follow("sdfwergwghr","Drand1943")
    # print(imagesForUser("Giarturner"))
    # print(getUserFollowers("Cagoo1938"))
    # print(getImagesToShow("Ristraid"))
    # addUser("robadobbob", "1234567890!!lol", "robbiieeee@gamil.com", "Robert", "Tobert")
    # copy_plaintext_passwords()
    # hash_passwords()
    # populateFollowerDatabase()
    # print(getUserFollowers("Drand1943"))
    # print(getusers())
    # populateImageDatabse()
    print(imagesForUser("Thithe"))
