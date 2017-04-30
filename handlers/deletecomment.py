from handler import Handler
from models import Comments

class DeleteComment(Handler):
    def get(self):
        self.error(404)

    def post(self):
        comment_id = int(self.request.get("cid"))

        comment = Comments.by_id(comment_id)
        blog_id = comment.blog_id
        if comment and comment.username == self.user:
            comment.delete()

        self.redirect("/post/%s" % blog_id)
