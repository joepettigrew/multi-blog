from google.appengine.ext import db


class Blogs(db.Model):
    """ Blogs entity in Google Datastore"""
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
