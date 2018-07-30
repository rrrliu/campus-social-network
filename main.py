# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
import urllib
import urllib2
import os
from model import User



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/index.html')

        dp_url = self.request.get('dp_url')
        email = self.request.get('email')
        f_name = self.request.get('first_name')
        l_name = self.request.get('last_name')

        user = User(first_name = f_name,
                    last_name = l_name,
                    dp_url = dp_url,
                    email = email)
        user.put()

        

        self.response.write(results_template.render())
    # def post(self):
    #     results_template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    #
    #     text = self.request.get('text')
    #     img_url = self.request.get('img_url')
    #     type = self.request.get('type')
    #
    #     post = Post(text = text,
    #                 img_url = img_url,
    #                 type = type)
    #
    #     post.put()
        # img_url = meme.get_meme_url()
        # all_memes = Meme.query().fetch()
        #
        # the_variable_dict = { 'line1' : meme_first_line,
        #                       'line2' : meme_second_line,
        #                       'img_url' : img_url,
        #                       'all_memes' : all_memes }
        #
        # self.response.write(results_template.render())

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(results_template.render())


class ProfilePage(webapp2.RequestHandler):
    def get(self):
        results_template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        self.response.write(results_template.render())
    # def login(self):
    #


app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/index', MainPage),
    ('/profile', ProfilePage)
], debug=True)
