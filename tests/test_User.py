from user import User
import mysql.connector
import datetime
import mysql
db = mysql.connector.connect(
    host='184.144.173.26',
    user='root',
    passwd='Binstagram_341',
    database='binstagram'
)

user = User.get_from_db(db, 'id', 3)


def test_get_followable():
    """Tests list of all followable users"""
    followable = User.get_followable(user, db)
    known_followable = {'Ablion73': 'follow', 'alexabarra': 'follow', 'Arman1992': 'unfollow', 'Bods1940': 'follow', 'Calasts53': 'follow', 'Careekeres': 'follow', 'Carther1949': 'unfollow', 'Cathery': 'follow', 'CItester': 'follow', 'Crinsonast1984': 'follow', 'Dideas85': 'follow', 'Drand1943': 'follow', 'Facepow': 'follow', 'Feck1968': 'follow', 'Gaveressake': 'follow', 'Giarturner': 'follow', 'Goiderearsur': 'follow', 'Hadet1965': 'follow', 'Hiserus': 'follow', 'Horgy1990': 'unfollow', 'Hurs1997': 'follow', 'Jonathan': 'follow', 'Kning1982': 'follow', 'kylejen': 'follow', 'Locies': 'unfollow', 'Marknow': 'follow',
           'MatteoGisondi': 'follow', 'Milloon': 'unfollow', 'Myseat': 'follow', 'Prempeh': 'follow', 'Ristraid': 'follow', 'Sequith': 'unfollow', 'Slogummid': 'follow', 'Somprood': 'follow', 'Sone1983': 'follow', 'Suchown': 'follow', 'Sups1944': 'follow', 'Swentorme1935': 'unfollow', 'Thdow1971': 'follow', 'Thensted': 'follow', 'Thetting': 'follow', 'Theyear': 'follow', 'Togand': 'follow', 'Trumsess1943': 'follow', 'Usithed66': 'follow', 'Weaught': 'unfollow', 'Weververnly': 'follow', 'Whatithas': 'follow', 'Whimseeplis': 'unfollow', 'Wilegire1937': 'follow', 'Winglersen1989': 'follow', 'Witive': 'follow', 'Wrove1935': 'follow'}
    assert followable == known_followable


def test_get_usernames():
    """Returns all usernames in database"""
    usernames = ['Ablion73', 'alexabarra', 'Arman1992', 'Bods1940', 'Calasts53', 'Careekeres', 'Carther1949', 'Cathery', 'CItester', 'Crinsonast1984', 'Dideas85', 'Drand1943', 'Facepow', 'Feck1968', 'Gaveressake', 'Giarturner', 'Goiderearsur', 'Hadet1965', 'Hiserus', 'Horgy1990', 'Hurs1997', 'Jonathan', 'Kning1982', 'kylejen', 'Locies', 'Marknow',
           'MatteoGisondi', 'Milloon', 'Myseat', 'Prempeh', 'Ristraid', 'Sequith', 'Slogummid', 'Somprood', 'Sone1983', 'Suchown', 'Sups1944', 'Swentorme1935', 'Thdow1971', 'Thensted', 'Thetting', 'Theyear', 'Thithe', 'Togand', 'Trumsess1943', 'Usithed66', 'Weaught', 'Weververnly', 'Whatithas', 'Whimseeplis', 'Wilegire1937', 'Winglersen1989', 'Witive', 'Wrove1935']
    assert User.get_usernames(db) == usernames


def test_get_likes():
    """Returns combined likes a user has on their posts"""
    assert user.get_likes(db) == 7


def test_get_user():
    """Returns all information pertaining to a user"""
    user_thithe = (3, 'Thithe', 'GeneCRodriguez@dayrep.com', 'Gene',
           'Rodriguez', '$2b$12$TtGou.MWZbzVaZMZPFE74eXcmcEKlPQMYS5cvBgJyCiOj3F5ey.4S')
    assert User.get_user(user) == user_thithe


def test_is_followable():
    """Tests if a user can be followed by another user"""
    user2 = User.get_from_db(db, 'id', 4)
    assert User.is_followable(user, user2)


def test_get_following():
    """Check if users following a user in bd are defined properly"""
    users = user.get_following(db)
    usernames = set(map(lambda x: x.username, users))
    known_usernames = {'Arman1992', 'Milloon', 'Swentorme1935', 'Whimseeplis',
           'Horgy1990', 'Weaught', 'Horgy1990', 'Sequith', 'Locies', 'Carther1949'}
    assert usernames == known_usernames


def test_get_followers():
    """Check if followers for a user in bd are defined properly"""
    users = user.get_followers(db)
    usernames = set(map(lambda x: x.username, users))
    known_usernames = {'Theyear', 'Marknow', 'Facepow', 'Hadet1965', 'Hadet1965',
           'Hiserus', 'Cathery', 'Sups1944', 'Slogummid', 'Sone1983', 'MatteoGisondi', 'Prempeh'}
    assert usernames == known_usernames
