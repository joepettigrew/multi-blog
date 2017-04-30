from handler import Handler
from models import Blogs
from models import Comments

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

        self.redirect("/post/%s" % blog_id)
