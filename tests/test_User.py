from user import User
from post import Post
import mysql.connector
import datetime
db = mysql.connector.connect(
    host='184.144.173.26',
    user='root',
    passwd='Binstagram_341',
    database='binstagram'
)
user = User.get_from_db(db,'id',3)
post = Post.get_by_id(db, 3)
comment = 

def test_get_usernames(): #Returns all usernames in database
    assert(User.get_usernames(db) == ['Ablion73', 'alexabarra', 'Arman1992', 'Bods1940', 'Calasts53', 'Careekeres', 'Carther1949', 'Cathery', 'CItester', 'Crinsonast1984', 'Dideas85', 'Drand1943', 'Facepow', 'Feck1968', 'Gaveressake', 'Giarturner', 'Goiderearsur', 'Hadet1965', 'Hiserus', 'Horgy1990', 'Hurs1997', 'Jonathan', 'Kning1982', 'kylejen', 'Locies', 'Marknow', 'MatteoGisondi', 'Milloon', 'Myseat', 'Prempeh', 'Ristraid', 'Sequith', 'Slogummid', 'Somprood', 'Sone1983', 'Suchown', 'Sups1944', 'Swentorme1935', 'Thdow1971', 'Thensted', 'Thetting', 'Theyear', 'Thithe', 'Togand', 'Trumsess1943', 'Usithed66', 'Weaught', 'Weververnly', 'Whatithas', 'Whimseeplis', 'Wilegire1937', 'Winglersen1989', 'Witive', 'Wrove1935'])
    
def test_get_likes(): #Returns combined likes a user has on their posts
    assert( user.get_likes(db)== 7)

def test_get_user(): #Returns all information pertaining to a user
    assert(User.get_user(user) == (3, 'Thithe', 'GeneCRodriguez@dayrep.com', 'Gene', 'Rodriguez', '$2b$12$TtGou.MWZbzVaZMZPFE74eXcmcEKlPQMYS5cvBgJyCiOj3F5ey.4S'))

def test_is_followable(): #Tests if a user can be followed by another user
    user2 = User.get_from_db(db,'id',4)
    assert(User.is_followable(user,user2) == True)

def test_get_user_likes():
    assert(Post.get_user_likes(post,db) == ['Ablion73', 'Whimseeplis', 'Marknow', 'Crinsonast1984'])



    



