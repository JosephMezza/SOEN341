from post import Post, Comment
from user import User
from base64 import b64encode
import mysql.connector
import datetime
import os
db = mysql.connector.connect(
    host='184.144.173.26',
    user='root',
    passwd='Binstagram_341',
    database='binstagram'
)
post = Post.get_by_id(db, 3)

def test_get_user_likes(): 
    assert(post.get_user_likes(db) == ['Ablion73', 'Whimseeplis', 'Marknow', 'Crinsonast1984'])

def test_get_user():
    user = User.get_from_db(db, 'id', 40)
    assert(post.get_user(db) == user)

def test_get_post_comments():
    post_comments = Comment.get_post_comments(db,post)
    s1 = str(post_comments['alexabarra'])
    assert( s1 == 'Nice Pic')
def test_like():
    likes = len(post.get_user_likes(db))
    print(likes)
    user = User.get_from_db(db,'id',3)
    print(user)
    post.like(db,user)
    post.unlike(db,user)
    assert(len(post.get_user_likes(db)) == likes)
