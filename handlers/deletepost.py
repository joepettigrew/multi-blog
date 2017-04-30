from handler import Handler
from models import Blogs

class DeletePost(Handler):
    def get(self):
        self.error(404)

    def post(self):
        blog_id = self.request.get("bid")
        if Blogs.verify_owner(blog_id, self.user):
            blog = Blogs.by_id(blog_id)
            blog.delete()
            self.redirect("/welcome")
        else:
            self.redirect("/welcome")
