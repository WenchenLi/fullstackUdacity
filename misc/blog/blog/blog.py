import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class Main(BaseHandler):
    """docstring for Main"""
    def get(self):
        self.render("index.html")

class Rot13(BaseHandler):
    def get(self):
        self.render('rot.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot.html', text = rot13)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):

    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        confirm = self.request.get('confirm')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['hint_username'] = "not a valid username."
            have_error = True

        if not valid_password(password):
            params['hint_password'] = "not a valid password."
            have_error = True
        elif password != confirm:
            params['hint_confirm'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['hint_email'] = "not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')


class BlogWrite(BaseHandler):

    def get(self):
        self.render("write.html")

    def post(self):
        have_error = False
        title = self.request.get('title')
        content = self.request.get('content')


        params = dict(title = title,
                      content = content)

        if not title:
            params['hint_title'] = "title is needed"
            have_error = True

        if not content:
            params['hint_content'] = "no blog is without content right?"
            have_error = True

        if have_error:
            self.render('write.html', **params)
        else:
            blog = Blog(title = title, content = content)
            blog.put()
            self.redirect('/blog/front')

class BlogFront(BaseHandler):
    def render_front(self):
        blogs = db.GqlQuery("SELECT * FROM Blog "
                            "ORDER BY created DESC ")
        self.render("front.html",blogs = blogs)

    def get(self):
        self.render_front()

    def write(self):
        self.redirect("/blog/write")

def blog_key(name = "defualt"):
    return db.Key.from_path("blogs",name)

class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

app = webapp2.WSGIApplication([('/', Main),
                                ('/blog/front', BlogFront),
                                ('/blog/write', BlogWrite),
                                ('/rot13', Rot13),
                               ('/signup', Signup),
                               ('/welcome', Welcome)],
                              debug=True)
