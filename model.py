from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    dp_url = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    # id = ndb.IntegerProperty(required=True)

class Post(ndb.Model):
    # author_id = ndb.IntegerProperty(required=True)
    author_key = ndb.KeyProperty(User)
    text = ndb.StringProperty(required=True)
    img_url = ndb.StringProperty(required=True)
    timestamp = ndb.StringProperty(required=True)
    score = ndb.IntegerProperty(required=True)
    author_name = ndb.StringProperty(required=True)
    author_pic = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)

class Comment(ndb.Model):
    author_key = ndb.KeyProperty(User)
    post_key = ndb.KeyProperty(Post)
    text = ndb.StringProperty(required=True)
    author_name = ndb.StringProperty(required=True)
