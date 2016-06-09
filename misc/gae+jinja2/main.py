import webapp2,string,jinja2
import os
from signup import *

template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape = True)

class Handler(webapp2.RequestHandler):
	"""base jinja template handler """
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))


class MainPage(Handler):
    """Mainpage"""
    def get(self):
		self.render("child.html")

class SignupPage(Handler):
    """Signup page"""
    def get(self):
		self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        password_confirm = self.request.get('password_confirm')
        email = self.request.get('email')

        if not (username and password and password_confirm):
            self.render("signup.html",hint = "one of the required field is missing!")
            return
        elif password != password_confirm:
            self.render("signup.html",hint_password_confirm = "password does not match")
            return

        u = valid_username(username)
        p = valid_password(password)
        p_c = valid_password(password_confirm)
        e = valid_email(email)

        if not u:
            self.render("signup.html",hint_username = "username is not valid")
            return
        elif not p:
            self.render("signup.html",hint_password = "password is not valid")
            return
        elif email and not e:
            self.render("signup.html",hint_email = "email is not valid")
            return
        else:
            self.redirect("/welcome?username="+username)

class WelcomePage(Handler):
    """docstring for WelcomePage"""
    def get(self):
		username = self.request.get("username")
		if valid_username(username):
			self.render("welcome.html",username=username)
		else:
			self.redirect("/signup")

class RotPage(Handler):
    """docstring for RotPage"""

    def get(self):
    	self.render("rot.html")

    def post(self):
    	text = self.request.get("text")
    	self.render("rot.html",text = self.rot_x(text))

    def rot_x(self,text,x=13):
    	t =  str(text)
    	punct_space_set = set(string.punctuation)
    	punct_space_set.add(" ")
    	res = []
    	for c in t:
    		if c.islower():#lower case char
    			res.append(chr((ord(c)-ord('a')+13)%26+ord('a')))
    		elif c.isupper():#upper case char
    			res.append(chr((ord(c)-ord('A')+13)%26+ord('A')))
    		elif c in punct_space_set or c.isdigit():#space and puntuation
    			res.append(c)
    	return "".join(res)

app = webapp2.WSGIApplication([('/', MainPage),('/signup,',SignupPage),('/rot,',RotPage),('/welcome,',WelcomePage)], debug=True)

# app = webapp2.WSGIApplication([('/signup', SignupPage),('/welcome,',WelcomePage)], debug=True)
