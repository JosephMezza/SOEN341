import csv
from follower import getListFromCSV, addUser,getusers,imagesForUser,getUserFollowers,getImagesToShow

#Tests if reading data from a CSV works properly
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

#Tests if we returning a list of all users works properly
def test_getUsers():
    assert getusers() == ['Ablion73', 'Winglersen1989', 'Thithe', 'Wrove1935', 'Kning1982', 'Whimseeplis', 'Locies', 'Somprood', 'Giarturner', 'Drand1943', 'Theyear', 'Witive', 'Ristraid', 'Dideas85', 'Milloon', 'Calasts53', 'Usithed66', 'Marknow', 'Feck1968', 'Suchown', 'Thensted', 'Crinsonast1984', 'Weaught', 'Weververnly', 'Trumsess1943', 'Bods1940', 'Facepow', 'Gaveressake', 'Careekeres', 'Togand', 'Hadet1965', 'Carther1949', 'Hiserus', 'Swentorme1935', 'Cathery', 'Sups1944', 'Wilegire1937', 'Thetting', 'Hurs1997', 'Goiderearsur', 'Thdow1971', 'Horgy1990', 'Sequith', 'Myseat', 'Slogummid', 'Sone1983', 'Whatithas', 'Arman1992', 'alexabarra', 'Jonathan'] 

#Tests if the proper list of images is returned for a specific user
def test_imagesForUser():
    assert imagesForUser('Ablion73') == ['img(1).jpg', 'img(2).jpg', 'img(3).jpg', 'img(4).jpg', 'img(5).jpg']

#Tests if the getUserFollowers methods returns the correct followers of a user
def test_getUserFollowers():
    assert getUserFollowers('Ablion73') == ['Feck1968', 'Myseat', 'Calasts53', 'Arman1992', 'Witive', 'Suchown', 'Locies', 'Witive', 'Hadet1965', 'Winglersen1989', 'alexabarra']

#Tests if the proper images that will be displayed on the home page
def test_getImagesToShow():
    assert getImagesToShow('Ablion73') == ['img(91).jpg', 'img(92).jpg', 'img(93).jpg', 'img(94).jpg', 'img(95).jpg', 'img(216).jpg', 'img(217).jpg', 'img(218).jpg', 'img(219).jpg', 'img(220).jpg', 'img(76).jpg', 'img(77).jpg', 'img(78).jpg', 'img(79).jpg', 'img(80).jpg', 'img(236).jpg', 'img(237).jpg', 'img(238).jpg', 'img(239).jpg', 'img(240).jpg', 'img(56).jpg', 'img(57).jpg', 'img(58).jpg', 'img(59).jpg', 'img(60).jpg', 'img(96).jpg', 'img(97).jpg', 'img(98).jpg', 'img(99).jpg', 'img(100).jpg', 'img(31).jpg', 'img(32).jpg', 'img(33).jpg', 'img(34).jpg', 'img(35).jpg', 'img(56).jpg', 'img(57).jpg', 'img(58).jpg', 'img(59).jpg', 'img(60).jpg', 'img(151).jpg', 'img(152).jpg', 'img(153).jpg', 'img(154).jpg', 'img(155).jpg', 'img(6).jpg', 'img(7).jpg', 'img(8).jpg', 'img(9).jpg', 'img(10).jpg', 'img(241).jpg', 'img(242).jpg', 'img(243).jpg', 'img(244).jpg', 'img(245).jpg']