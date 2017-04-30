from google.appengine.ext import db
from functools import wraps


def post_exists_wrap(function):
    @wraps(function)
    def wrapper(self, blog_id):
        key = db.Key.from_path("Blogs", int(blog_id))
        blog = db.get(key)
        if blog:
            return function(self, blog_id)
        else:
            self.error(404)
            return
    return wrapper


def comment_exists(cid):
    key = db.Key.from_path("Comments", int(cid))
    return db.get(key)


def post_exists(cid):
    key = db.Key.from_path("Blogs", int(cid))
    return db.get(key)
