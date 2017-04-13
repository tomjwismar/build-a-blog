#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("blogpage.html")
        content = t.render()
        self.response.write(content)
    def post(self):
        t = jinja_env.get_template("newposts.html")
        content = t.render()
        self.respone.write(content)


app = webapp2.WSGIApplication([
    ('/blog', MainHandler),
    ('/newposts',MainHandler)
], debug=True)
