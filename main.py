
import webapp2
import jinja2
import urllib
import urllib2
import os
from model import User, Post
from datetime import datetime
import time
import pytz



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
            self.session['key'] = user.put()
        # else:
            # self.session['key'] = User.query(User.email === user.email)

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

        if not (len(text) == 0 and len(img_url) == 0):
            current_time = datetime.now()

            post = Post(text = text,
                        img_url = img_url,
                        type = type,
                        timestamp = current_time,
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
            'email' : self.session.get('email'),
            'dp_url' : self.session.get('dp_url'),
        }
        self.response.write(results_template.render(info))
    def post(self):
        # user_obj = self.session.get('key').get()

        self.session['dp_url'] = self.request.get('dp_url')
        self.session['email'] = self.request.get('email')
        self.session['f_name'] = self.request.get('first_name')
        self.session['l_name'] = self.request.get('last_name')

        # user_obj.dp_url = self.request.get('dp_url')
        # user_obj.email = self.request.get('email')
        # user_obj.first_name = self.request.get('first_name')
        # user_obj.last_name = self.request.get('last_name')
        # user_obj.put()

        self.redirect('/index')

class LoginHandler(BaseHandler):
    def post(self):
        self.session['dp_url'] = self.request.get('dp_url')
        self.session['email'] = self.request.get('email')
        self.session['f_name'] = self.request.get('first_name')
        self.session['l_name'] = self.request.get('last_name')
        self.redirect('/index')

class AboutUsHandler(BaseHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/aboutUs.html')
        self.response.write(results_template.render())



config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/index', MainHandler),
    ('/profile', ProfileHandler),
    ('/login', LoginHandler),
    ('/aboutus', AboutUsHandler),
], config=config,
   debug=True)
