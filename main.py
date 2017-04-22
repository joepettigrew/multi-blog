import os
import jinja2
import webapp2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# User entity in Google Datastore
class Users(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


# Blog entity in Google Datastore
class Blogs(db.Model):
    # username = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    blog_post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC")
        self.render("index.html", blogs=blogs)


# Username validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

# Password validation
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

# Email validation
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# Get Username from DB
def query_username(username):
    user = db.GqlQuery("SELECT * FROM Users WHERE username = :1", username)
    result = user.get()
    return result.username


class SignUpPage(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['error_username'] = "Invalid username"
            have_error = True

        if not valid_password(password):
            params['error_password'] = "Invalid password"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords didn't match"
            have_error = True

        if not valid_email(email):
            params['error_email'] = "Invalid email address"
            have_error = True

        if have_error:
            self.render("signup.html", **params)
        else:
            user = Users(username=username, password=password, email=email)
            user.put()
            self.redirect("/welcome?username=" + username)


class WelcomePage(Handler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            user = query_username(username)
            self.render("welcome.html", username=user)
        else:
            self.redirect("/signup")


class BlogPost(Handler):
    def get(self):
        self.render("blogpost.html")

    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("post")

        if title and blog_post:
            blog = Blogs(title=title, blog_post=blog_post)
            blog.put()
            self.redirect("/")
        else:
            error = "We need both the title and the blog post."
            self.render("blogpost.html", title=title, blog_post=blog_post, error=error)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignUpPage),
    ('/welcome', WelcomePage),
    ('/blogpost', BlogPost)
], debug=True)
