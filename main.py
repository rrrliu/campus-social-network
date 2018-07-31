
import webapp2
import jinja2
import urllib
import urllib2
import os
from model import User, Post
import datetime
import time


import webapp2

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
        results_template = JINJA_ENVIRONMENT.get_template('templates/index.html')

        user = User(first_name = self.session.get('f_name'),
                    last_name = self.session.get('l_name'),
                    dp_url = self.session.get('dp_url'),
                    email = self.session.get('email'),)
        if not (User.query(User.email == user.email).fetch()):
            user.put()

        all_posts = Post.query().fetch()
        info = {
            'first_name' : self.session.get('f_name'),
            'last_name' : self.session.get('l_name'),
            'dp_url' : self.session.get('dp_url'),
            'email' : self.session.get('email'),
            'all_posts' : all_posts,
        }

        self.response.write(results_template.render(info))

    def post(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/index.html')

        text = self.request.get('text')
        img_url = self.request.get('img_url')
        type = self.request.get('type')

        author_name = self.session.get('f_name') + ' ' + self.session.get('l_name')
        author_pic = self.session.get('dp_url')

        if len(text) == 0 and len(img_url) == 0:
            self.redirect('/')

        post = Post(text = text,
                    img_url = img_url,
                    type = type,
                    timestamp = datetime.datetime.now(),
                    author_name = author_name,
                    author_pic = author_pic)
        post.put()
        time.sleep(0.5)
        self.redirect('/index')

class WelcomeHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(results_template.render())


class ProfileHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        info = {
            'first_name' : self.session.get('f_name'),
            'last_name' : self.session.get('l_name'),
            'dp_url' : self.session.get('dp_url'),
        }
        self.response.write(results_template.render(info))
    # def login(self):
    #

class LoginHandler(BaseHandler):
    def post(self):
        self.session['dp_url'] = self.request.get('dp_url')
        self.session['email'] = self.request.get('email')
        self.session['f_name'] = self.request.get('first_name')
        self.session['l_name'] = self.request.get('last_name')
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
], config=config,
   debug=True)
