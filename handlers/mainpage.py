from handler import Handler
from models import Blogs


class MainPage(Handler):
    """Renders home page with blog posts"""
    def get(self):
        blogs = Blogs.all().order("-created")
        self.render("/index.html", blogs=blogs, auth_user=self.user)
