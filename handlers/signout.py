from handler import Handler


class SignOut(Handler):
    """Logs user out"""
    def get(self):
        if self.user:
            self.logout()
        self.redirect("/signup")
