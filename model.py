from google.appengine.ext import ndb

class User:
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    dp_url = ndb.StringProperty(required=True)
    id = ndb.IntegerProperty(required=True)

class Post:
    # author_id = ndb.IntegerProperty(required=True)
    # author_key = ndb.KeyProperty(User)
    text = ndb.StringProperty(required=True)
    img_url = ndb.StringProperty(required=True)
    # timestamp = ndb.DateTimeProperty(required=True)
    # score = ndb.IntegerProperty(required=True)
    # comments = ndb.StringProperty(repeated=True)
    type = ndb.StringProperty(required=True)
