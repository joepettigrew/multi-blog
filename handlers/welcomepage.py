from handlers import Handler
from models import Blogs


class WelcomePage(Handler):
    def get(self):
        params = dict(auth_user=self.user)
        params['blogs'] = Blogs.all().filter("username = ",
                                             self.user).order("-created")
        self.user_page("welcome.html", "/signup", **params)
