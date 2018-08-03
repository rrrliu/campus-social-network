import webapp2
import jinja2
import urllib
import urllib2
import os
from model import User, Post, Comment, Like
from datetime import datetime
import time
import json
from google.appengine.ext.ndb import Key
from google.appengine.ext import ndb


from webapp2_extras import sessions

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(BaseHandler):
    def get(self):
        if (self.session.get('email') == None):
            self.redirect('/')

        results_template = JINJA_ENVIRONMENT.get_template('templates/index.html')

        user = User(first_name = self.session.get('f_name'),
                    last_name = self.session.get('l_name'),
                    dp_url = self.session.get('dp_url'),
                    email = self.session.get('email'),)
        if not (User.query(User.email == user.email).fetch()):
            self.session['user_key_id'] = user.put().id()
        else:
            self.session['user_key_id'] = User.query(User.email == user.email).fetch()[0].key.id()
        all_users = User.query().fetch()
        all_posts = Post.query().order(-Post.date_time).fetch()
        all_comments = Comment.query().order(Comment.date_time).fetch()
        info = {
            'first_name' : self.session.get('f_name'),
            'last_name' : self.session.get('l_name'),
            'dp_url' : self.session.get('dp_url'),
            'email' : self.session.get('email'),
            'all_posts' : all_posts,
            'all_users' : all_users,
            'all_comments' : all_comments
        }

        self.response.write(results_template.render(info))

    def post(self):
        text = self.request.get('text')
        img_url = self.request.get('img_url')
        type = self.request.get('type')

        if not (len(text) == 0 and len(img_url) == 0):

            key_id = self.session.get('user_key_id')
            key = Key('User', key_id)

            author_name = self.session.get('f_name') + ' ' + self.session.get('l_name')
            author_pic = self.session.get('dp_url')

            utc_dt = datetime.now()
            # local_tz = pytz.timezone('US/Pacific')
            # local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
            updated_hour = utc_dt.hour - 7
            if utc_dt.hour < 7:
                updated_hour += 24
            local_dt = utc_dt.replace(hour=updated_hour)
            format = '%A at %I:%M %p'
            current_time = local_dt.strftime(format)
            # current_time = utc_dt.strftime(format)

            post = Post(author_key = key,
                        text = text,
                        img_url = img_url,
                        type = type,
                        timestamp = current_time,
                        author_name = author_name,
                        author_pic = author_pic,
                        score = 0,
                        date_time = datetime.now().strftime('%m/%d/%y/%H/%M/%S/%f'))
            post.put()
            time.sleep(0.1)
        self.redirect('/index')

class WelcomeHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(results_template.render())


class ProfileHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        all_posts = Post.query().fetch()
        user_key = Key('User', self.session.get('user_key_id'))
        user_posts = Post.query(Post.author_key == user_key).fetch()
        all_comments = Comment.query().fetch()
        info = {
            'first_name' : self.session.get('f_name'),
            'last_name' : self.session.get('l_name'),
            'email' : self.session.get('email'),
            'dp_url' : self.session.get('dp_url'),
            'user_posts' : user_posts,
            'all_comments' : all_comments
        }
        self.response.write(results_template.render(info))
    def post(self):
        user_key = Key('User', self.session.get('user_key_id'))
        user_obj = user_key.get()

        self.session['dp_url'] = self.request.get('dp_url')
        self.session['email'] = self.request.get('email')
        self.session['f_name'] = self.request.get('first_name')
        self.session['l_name'] = self.request.get('last_name')

        user_obj.dp_url = self.request.get('dp_url')
        user_obj.email = self.request.get('email')
        user_obj.first_name = self.request.get('first_name')
        user_obj.last_name = self.request.get('last_name')
        user_obj.put()

        time.sleep(0.1)
        self.redirect('/index')

class LoginHandler(BaseHandler):
    def post(self):
        self.session['dp_url'] = self.request.get('dp_url')
        self.session['email'] = self.request.get('email')
        self.session['f_name'] = self.request.get('first_name')
        self.session['l_name'] = self.request.get('last_name')
        self.redirect('/index')

class LogoutHandler(BaseHandler):
    def get(self):
        self.session['dp_url'] = None
        self.session['email'] = None
        self.session['f_name'] = None
        self.session['l_name'] = None
        self.redirect('/')
    # def post(self):
    #     self.session['dp_url'] = None
    #     self.session['email'] = None
    #     self.session['f_name'] = None
    #     self.session['l_name'] = None
    #     self.redirect('/')

class AboutUsHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/aboutUs.html')
        self.response.write(results_template.render())

class DeleteHandler(BaseHandler):
    def post(self):
        # my_post = self.request.get('postDiv')
        # my_obj = Post.query(User.key == my_post.key).fetch()[0]
        # my_obj.delete()
        # time.sleep(0.1)
        self.redirect('/index')

class LikeHandler(BaseHandler):
    def post(self):
        date_time = self.request.get('date_time')
        post_key = Post.query(Post.date_time == date_time).fetch()[0].key
        post = post_key.get()
        query = Like.query(Like.post_key == post.key).fetch()
        like_author = None
        author_key = Key('User', self.session.get('user_key_id'))
        if len(query) > 0:
            like_author = query[0].author_key
        # if not (User.query(User.email == user.email).fetch()):
        if not (like_author == author_key):
            score = self.request.get('score')
            post.score = int(score) + 1

            Like(author_key = author_key,
                 post_key = post_key).put()
        post.put()
        time.sleep(0.1)
        self.redirect('/index')

class CommentHandler(BaseHandler):
    def post(self):
        text = self.request.get('comment')
        if len(text) > 0:
            date_time = self.request.get('date_time')
            post_key = Post.query(Post.date_time == date_time).fetch()[0].key
            name = self.request.get('author_name')
            author_key = Key('User', self.session.get('user_key_id'))
            comment = Comment(author_key = author_key,
                              post_key = post_key,
                              text = text,
                              author_name = name,
                              date_time = datetime.now().strftime('%m/%d/%y/%H/%M/%S/%f'))
            comment.put()
            time.sleep(0.1)
        self.redirect('/index')

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/index', MainHandler),
    ('/profile', ProfileHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/aboutus', AboutUsHandler),
    ('/delete', DeleteHandler),
    ('/like', LikeHandler),
    ('/comment', CommentHandler),
], config=config,
   debug=True)
