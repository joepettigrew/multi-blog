from handler import Handler


class SignOut(Handler):
    def get(self):
        if self.user:
            self.logout()
        self.redirect("/signup")
