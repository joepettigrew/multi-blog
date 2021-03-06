from google.appengine.ext import db


class Sentiment(db.Model):
    """Interactions entity in Google Datstore"""
    username = db.StringProperty()
    blog_id = db.IntegerProperty()
    sentiment = db.BooleanProperty()

    @classmethod
    def by_owner(cls, username, blog_id):
        sentiment = cls.all().filter("username = ", username)
        sentiment = sentiment.filter("blog_id = ", int(blog_id)).get()
        return sentiment
