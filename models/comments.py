from google.appengine.ext import db


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
