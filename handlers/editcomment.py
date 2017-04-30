from handler import Handler
from models import Blogs, Comments
from util import comment_exists


class EditComment(Handler):
    """Edits comment for auth users"""
    def get(self):
        self.error(404)

    def post(self):
        comment_id = int(self.request.get("cid"))
        comment_text = self.request.get("comment")
        blog_id = int(self.request.get("bid"))

        # Checks user's auth status and comment exists
        if self.user and comment_exists(comment_id):
            comment = Comments.by_id(comment_id)

            # Checks to see if user owns the comment
            if comment and comment.username == self.user:
                comment.comment = comment_text
                comment.put()

        self.redirect("/post/%s" % blog_id)
