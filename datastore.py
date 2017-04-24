from google.appengine.ext import db


# Users entity in Google Datastore
class Users(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

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
    username = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    updated = db.DateTimeProperty(auto_now = True)
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
class Interactions(db.Model):
    username = db.StringProperty()
    blog_id = db.IntegerProperty()
    sentiment = db.BooleanProperty()
    comment = db.TextProperty()
