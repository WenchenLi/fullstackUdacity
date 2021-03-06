"""
blog with basic features:
Site Usability:
1. User is directed to login, logout, and signup pages as appropriate. E.g.,
login page should have a link to signup page and vice-versa; logout page is
only available to logged in user.
2. Links to edit blog pages are available to users. Users editing a
page can click on a link to cancel the edit and go back to viewing that page.
3.Blog pages render properly. Templates are used to unify the site.

Accounts and Security:
1.Users are able to create accounts, login, and logout correctly.
2.Existing users can revisit the site and log back in without having to
recreate their accounts each time.
3.Usernames are unique. Attempting to create a duplicate user results
in an error message.
4.Stored passwords are hashed. Passwords are appropriately checked during
login. User cookie is set securely.

Permissions:
1.Logged out users are redirected to the login page when attempting
to create, edit, delete, or like a blog post.
2.Logged in users can create, edit, or delete blog posts they
themselves have created.
Users should only be able to like posts once and should not be
able to like their own post.
3. Only signed in users can post comments.Users can only edit
and delete comments they themselves have made.
"""

import webapp2
import time
from template_setup import *
from database import *
from regexp import *
import datetime
import constant

class BlogHandler(webapp2.RequestHandler):
    """base handler"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return template_render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        self.set_secure_cookie('expires', str((datetime.datetime.now() +
            datetime.timedelta(weeks=2)).strftime('%a, %d %b %Y %H:%M:%S GMT')))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class BlogFront(BlogHandler):
    """blog frontpage"""
    def get(self):
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts)

class PostPage(BlogHandler):
    """page for read one post in detail"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comment.all()
        # comments.ancestor(comment_key())
        comments.filter('post_id =',str(post_id))
        comments.order('-created')
        if not post:
            self.error(404)
            return
        self.render("permalink.html", post=post,comments=comments)

    def post(self,post_id):
        comment_content = self.request.get('comment-content')
        if self.user and comment_content:
            c = Comment(parent=comment_key(), content=comment_content,
                        author=self.user.name, post_id=post_id)
            c.put()
            time.sleep(.5)#TODO callback once
            self.redirect('/blog/%s' % str(post_id))
        else:
            if not self.user:
                self.redirect('/login')
            else:
                self.response.out.write("please write something!")

class NewPost(BlogHandler):
    """page for write new post"""
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content,
                        author=self.user.name, likes=0)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject,
                            content=content, error=error)
class LikePost(BlogHandler):
    """likePosts handler"""
    def get(self, post_id):
        if self.user:
            self.render("front.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)
        if self.user:
            if self.user.name not in p.like_user:
                p.likes += 1
                p.like_user.append(self.user.name)
                p.put()
                time.sleep(.5)##TODO fix using calback
                self.redirect("/blog")
            else:
                self.response.out.write("you already liked this post!")
        else:
            self.redirect("/login")

class EditPost(BlogHandler):
    """page for edit previous post"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)

        if self.user:
            self.render("editpost.html", p=p)
        else:
            self.redirect("/login")


    def post(self,post_id):
        if not self.user:
            self.redirect('/blog')

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)

        p.subject = self.request.get('subject')
        p.content = self.request.get('content')

        if p.subject and p.content:
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("editpost.html", p=p, error=error)

class DeletePost(BlogHandler):
    """handler for delte previous post"""
    def get(self,post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)
        p.delete()
        time.sleep(.5)#TODO this is not idea, need to have callback once deleted from db,delete_async() might be good candidate
        self.redirect('/blog')

class EditComment(BlogHandler):
    """handler for edit previous comment"""
    def get(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id), parent=comment_key())
        c = db.get(key)

        if self.user:
            self.render("editcomment.html", c=c)
        else:
            self.redirect("/login")

    def post(self,comment_id):
        if not self.user:
            self.redirect('/blog')

        key = db.Key.from_path('Comment', int(comment_id), parent=comment_key())
        c = db.get(key)

        c.content = self.request.get('comment-content')
        if  c.content:
            c.put()
            time.sleep(.5)#TODO callback
            self.redirect('/blog/%s' % str(c.post_id))
        else:
            error = "subject and content, please!"
            self.render("editcomment.html", c=c, error=error)

class DeleteComment(BlogHandler):
    """handler for delte previous post"""
    def get(self,comment_id):
        key = db.Key.from_path('Comment', int(comment_id), parent=comment_key())
        c = db.get(key)
        c.delete()
        time.sleep(.5)#TODO this is not idea, need to have callback once deleted from db,delete_async() might be good candidate
        self.redirect('/blog/%s'% str(c.post_id))

class Signup(BlogHandler):
    """general purpose signup page without done implemented"""
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    """one inheritence of Signup"""
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/blog')

class Login(BlogHandler):
    """page login user"""
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)

class SigninPage(BlogHandler):
    def get(self):
        self.render('signin.html')

class Logout(BlogHandler):
    """logout handler"""
    def get(self):
        self.logout()
        self.redirect('/blog')

class Welcome(BlogHandler):
    """welcome/dashboard once user login"""
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', SigninPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/blog/edit/([0-9]+)', EditPost),
                               ('/blog/delete/([0-9]+)', DeletePost),
                               ('/blog/comment/edit/([0-9]+)', EditComment),
                               ('/blog/comment/delete/([0-9]+)', DeleteComment),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
