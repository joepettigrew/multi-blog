import os

# My files
import auth
from validate import Validate
from datastore import Users
from datastore import Blogs
from datastore import Sentiment
from datastore import Comments

import jinja2
import webapp2

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

    def set_secure_cookie(self, name, val):
        cookie_val = str(auth.make_secure_val(val))
        name = str(name)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; PATH=/" % (name, cookie_val)
        )

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and auth.check_secure_val(cookie_val)

    # Turns away unauthorized users
    def user_page(self, origin_page, alt_page, **kw):
        if self.user:
            self.render(origin_page, **kw)
        else:
            self.redirect(alt_page)

    # Turns away authorized users
    def anom_page(self, origin_page, alt_page, **kw):
        if self.user:
            self.redirect(alt_page)
        else:
            self.render(origin_page, **kw)

    # Log out (Deletes cookie)
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        auth_user = self.read_secure_cookie('username')
        self.user = auth_user and Users.by_username(auth_user)


class MainPage(Handler):
    def get(self):
        blogs = Blogs.all().order("-created")
        self.render("index.html", blogs=blogs, auth_user=self.user)


class SignUpPage(Handler):
    def get(self):
        self.anom_page("signup.html", "/welcome")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username, email=email)

        if not Validate(username).username():
            params['error_username'] = "Invalid username"
            have_error = True
        elif username == Users.by_username(username):
            params['error_username'] = "Same username already exists"
            have_error = True

        if not Validate(password).password():
            params['error_password'] = "Invalid password"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords didn't match"
            have_error = True

        if not Validate(email).email():
            params['error_email'] = "Invalid email address"
            have_error = True
        elif email and email == Users.by_email(email):
            params['error_email'] = "This email address is already used"
            have_error = True

        if have_error:
            self.render("signup.html", **params)
        else:
            # Create password hash
            pass_hash = auth.make_pw_hash(username, password)

            # Create user in DB
            user = Users(username=username, password=pass_hash, email=email)
            user.put()

            # Create cookie
            self.set_secure_cookie("username", username)

            # Redirect user to welcome page
            self.redirect("/welcome")


class LogIn(Handler):
    def get(self):
        self.anom_page("login.html", "/welcome")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")

        params = dict(username=username)

        if self.valid_cred(username, password):
            # Create cookie
            self.set_secure_cookie("username", username)

            # Redirect user to welcome page
            self.redirect("/welcome")
        else:
            have_error = True
            params['error_msg'] = "Invalid username or password"
            self.render("login.html", **params)

    def valid_cred(self, username, password, pass_hash=""):
        query = Users.all().filter("username", username).get()
        if query is not None:
            pass_hash = query.password
        return username and password and auth.valid_pw(username,
                                                       password,
                                                       pass_hash)


class LogOut(Handler):
    def get(self):
        self.logout()
        self.redirect("/")


class WelcomePage(Handler):
    def get(self):
        params = dict(auth_user=self.user)
        params['blogs'] = Blogs.all().filter("username = ",
                                             self.user).order("-created")
        self.user_page("welcome.html", "/signup", **params)


class BlogSubmit(Handler):
    def get(self):
        self.user_page("blogsubmit.html", "/signup", auth_user=self.user)

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        params = dict(auth_user=self.user, title=title, content=content)

        if title and content:
            # Remove <div> tag from posting
            content = content.replace("<div>", "")
            content = content.replace("</div>", "")

            # Add to Blogs entity
            blog = Blogs(title=title,
                         content=content,
                         username=self.user,
                         likes=0,
                         dislikes=0)
            blog.put()

            # Redirect to home page
            self.redirect("/welcome")
        else:
            params['error'] = "We need both the title and the blog post."
            self.render("blogsubmit.html", **params)


class EditPost(Handler):
    def get(self):
        params = dict(auth_user=self.user)
        blog_id = self.request.get("bid")
        if Blogs.verify_owner(blog_id, self.user):
            blog = Blogs.by_id(blog_id)
            params['blog_id'] = blog_id
            params['title'] = blog.title
            params['content'] = blog.content
            self.user_page("editpost.html", "/signup", **params)
        else:
            self.redirect("/welcome")

    def post(self):
        params = dict(auth_user=self.user)
        title = self.request.get("title")
        content = self.request.get("content")
        blog_id = self.request.get("bid")

        if title and content:
            # Remove <div> tag from posting
            content = content.replace("<div>", "")
            content = content.replace("</div>", "")

            # Update the Datastore
            blog = Blogs.by_id(blog_id)
            blog.title = title
            blog.content = content
            blog.put()

            # Redirect to home page
            self.redirect("/welcome")
        else:
            params['title'] = title
            params['content'] = content
            params['blog_id'] = blog_id
            params['error'] = "We need both the title and the blog post."
            self.render("editpost.html", **params)


class DeletePost(Handler):
    def get(self):
        self.error(404)

    def post(self):
        blog_id = self.request.get("bid")
        if Blogs.verify_owner(blog_id, self.user):
            blog = Blogs.by_id(blog_id)
            blog.delete()
            self.redirect("/welcome")
        else:
            self.redirect("/welcome")


class SinglePost(Handler):
    def get(self, blog_id):
        blog = Blogs.by_id(blog_id)
        sentiment = Sentiment.by_owner(self.user, blog_id)
        comments = Comments.by_blog_id(blog_id)

        params = dict(blog=blog,
                      sentiment=sentiment,
                      comments=comments,
                      auth_user=self.user)

        if not blog:
            self.error(404)
            return

        self.render("singlepost.html", **params)

    def post(self, blog_id):
        blog_id = int(self.request.get("bid"))
        comment = self.request.get("comment")
        blog = Blogs.by_id(blog_id)
        comments = Comments.by_blog_id(blog_id)
        sentiment = Sentiment.by_owner(self.user, blog_id)

        params = dict(blog_id=blog_id,
                      auth_user=self.user,
                      blog=blog,
                      comments=comments,
                      sentiment=sentiment)

        if not comment:
            params['error_comment'] = "You didn't write any comment!"
            self.render("singlepost.html", **params)
        else:
            comment = Comments(blog_id=blog_id,
                               comment=comment,
                               username=self.user)
            comment.put()
            self.redirect("/%s#Comments" % blog_id)


class LikePost(Handler):
    def get(self):
        blog_id = int(self.request.get("bid"))

        # Check to see if the user has interacted with this post before.
        sentiment = Sentiment.by_owner(self.user, blog_id)
        if sentiment is None:
            sentiment = Sentiment(username=self.user,
                                  blog_id=blog_id,
                                  sentiment=True)
            sentiment.put()

            # Update the Datastore
            blog = Blogs.by_id(blog_id)
            blog.likes += 1
            blog.put()

        self.redirect("/%s" % blog_id)


class DislikePost(Handler):
    def get(self):
        blog_id = int(self.request.get("bid"))

        # Check to see if the user has interacted with this post before.
        sentiment = Sentiment.by_owner(self.user, blog_id)
        if sentiment is None:
            sentiment = Sentiment(username=self.user,
                                  blog_id=blog_id,
                                  sentiment=False)
            sentiment.put()

            # Update the Datastore
            blog = Blogs.by_id(blog_id)
            blog.dislikes += 1
            blog.put()

        self.redirect("/%s" % blog_id)


class EditComment(Handler):
    def get(self):
        self.error(404)

    def post(self):
        comment_id = int(self.request.get("cid"))
        comment_text = self.request.get("comment")

        comment = Comments.by_id(comment_id)
        blog_id = comment.blog_id
        if comment and comment.username == self.user:
            comment.comment = comment_text
            comment.put()

        self.redirect("/%s" % blog_id)


class DeleteComment(Handler):
    def get(self):
        self.error(404)

    def post(self):
        comment_id = int(self.request.get("cid"))

        comment = Comments.by_id(comment_id)
        blog_id = comment.blog_id
        if comment and comment.username == self.user:
            comment.delete()

        self.redirect("/%s" % blog_id)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignUpPage),
    ('/welcome', WelcomePage),
    ('/([0-9]+)', SinglePost),
    ('/blogsubmit', BlogSubmit),
    ('/edit-post', EditPost),
    ('/delete-post', DeletePost),
    ('/like-post', LikePost),
    ('/dislike-post', DislikePost),
    ('/edit-comment', EditComment),
    ('/delete-comment', DeleteComment),
    ('/login', LogIn),
    ('/logout', LogOut)
], debug=True)
