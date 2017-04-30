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
