import webapp2,string,jinja2
import os

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

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
