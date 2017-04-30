from handler import Handler
from models import Comments
from util import comment_exists


class DeleteComment(Handler):
    def get(self):
        self.error(404)

    def post(self):
        comment_id = int(self.request.get("cid"))
        blog_id = int(self.request.get("bid"))

        # Checks user's auth status and comment exists
        if self.user and comment_exists(comment_id):
            comment = Comments.by_id(comment_id)

            # Checks to see if user owns the comment
            if comment and comment.username == self.user:
                comment.delete()

        self.redirect("/post/%s" % blog_id)
