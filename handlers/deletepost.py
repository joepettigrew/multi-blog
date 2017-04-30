from handler import Handler
from models import Blogs
from util import post_exists


class DeletePost(Handler):
    """Deletes blog posts for auth users"""
    def get(self):
        self.error(404)

    def post(self):
        blog_id = self.request.get("bid")

        # Check to see if post exists
        if post_exists(blog_id):

            # Check post ownership and auth status
            if self.user and Blogs.verify_owner(blog_id, self.user):
                blog = Blogs.by_id(blog_id)
                blog.delete()

        self.redirect("/welcome")
