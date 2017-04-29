from google.appengine.ext import db


# Users entity in Google Datastore
class Users(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_username(cls, username):
        user = cls.all().filter("username", username).get()
        return user and user.username

    @classmethod
    def by_email(cls, email):
        user = cls.all().filter("email", email).get()
        return user and user.email


# Blogs entity in Google Datastore
class Blogs(db.Model):
    username = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    likes = db.IntegerProperty()
    dislikes = db.IntegerProperty()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self._render_text

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(int(uid))

    @classmethod
    def verify_owner(cls, uid, username):
        if cls.get_by_id(int(uid)) is not None:
            owner_name = cls.get_by_id(int(uid)).username
            return owner_name == username


# Interactions entity in Google Datstore
class Sentiment(db.Model):
    username = db.StringProperty()
    blog_id = db.IntegerProperty()
    sentiment = db.BooleanProperty()

    @classmethod
    def by_owner(cls, username, blog_id):
        sentiment = cls.all().filter("username = ", username)
        sentiment = sentiment.filter("blog_id = ", int(blog_id)).get()
        return sentiment


# Comments entity in Google Datastore
class Comments(db.Model):
    username = db.StringProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(int(uid))

    @classmethod
    def by_blog_id(cls, blog_id):
        return cls.all().filter("blog_id = ", int(blog_id)).order("created")
