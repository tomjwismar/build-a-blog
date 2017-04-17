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

class Handler(webapp2.RequestHandler):
    def write (self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_blog(self,title="",blog="",error = ""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        self.render("blogpage.html",title = title,blog = blog,error = error,blogs = blogs)

    def get(self):
        self.render_blog()

class NewPost(Handler):
    def render_blog(self,title="",blog = "",error = ""):
        self.render("newposts.html",title = title, blog = blog, error = error)

    def get(self):
        self.render_blog()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            b = Blog(title=title, blog=blog)
            b.put()
            self.redirect('/blog/' + str(b.key().id()))
        else:
            error = "Enter both Title and Blog"
            self.render_blog(title,blog,error)

class ViewPostHandler(Handler):
    def render_blog(self,id,title = "",blog = "",error = ""):
        blog_post = Blog.get_by_id(int(id))
        self.render("single_post.html",title = title, blog = blog, error = error,blog_post = blog_post)

    def get(self,id):
        if id:
            self.render_blog(id)
        else:
            error = "Blog does not exist."
            self.render_blog(error = error)


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/newpost',NewPost),
    webapp2.Route('/blog/<id:\d+>',ViewPostHandler)
], debug=True)
