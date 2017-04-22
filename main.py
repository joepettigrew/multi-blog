import os
import re
import hashlib
import hmac
import random

import jinja2
import webapp2

from HTMLParser import HTMLParser
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

secret = "lkasdjf$j89u_345n45e-jtgdf8^459u23asd"

def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    if secure_val == make_secure_val(val):
        return val


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = str(make_secure_val(val))
        name = str(name)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; PATH=/" % (name, cookie_val)
        )


# Users entity in Google Datastore
class Users(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


# Blogs entity in Google Datastore
class Blogs(db.Model):
    # username = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    updated = db.DateTimeProperty(auto_now = True)


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
            # Create user in DB
            user = Users(username=username, password=password, email=email)
            user.put()

            # Create cookie
            self.set_secure_cookie("username", username)

            self.redirect("/welcome?username=" + username)


class WelcomePage(Handler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            user = query_username(username)
            self.render("welcome.html", username=user)
        else:
            self.redirect("/signup")


class BlogSubmit(Handler):
    def get(self):
        self.render("blogsubmit.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            # Add <br> automatically when a new line is created.
            content = content.replace('\n', '<br>')

            # Remove <p> tag from posting
            content = content.replace("<p>", "")
            content = content.replace("</p>", "")

            # Add to Datastore
            blog = Blogs(title=title, content=content)
            blog.put()

            # Redirect to home page
            self.redirect("/")
        else:
            error = "We need both the title and the blog post."
            self.render("blogsubmit.html", title=title, content=content, error=error)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignUpPage),
    ('/welcome', WelcomePage),
    ('/blogsubmit', BlogSubmit)
], debug=True)
