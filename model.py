from google.appengine.ext import ndb

class User:
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    dp_url = ndb.StringProperty(required=True)
