from handler import Handler
from models import Users
from models import Blogs
from models import Sentiment
from models import Comments

class MainPage(Handler):
    def get(self):
        blogs = Blogs.all().order("-created")
        self.render("/index.html", blogs=blogs, auth_user=self.user)
