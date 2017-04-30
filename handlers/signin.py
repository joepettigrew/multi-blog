from handler import Handler
import auth
from models import Users


class SignIn(Handler):
    """Signs in user after checking some hash"""
    def get(self):
        self.anom_page("login.html", "/welcome")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")

        params = dict(username=username)

        if self.valid_cred(username, password):
            # Create cookie
            self.set_secure_cookie("username", username)

            # Redirect user to welcome page
            self.redirect("/welcome")
        else:
            have_error = True
            params['error_msg'] = "Invalid username or password"
            self.render("login.html", **params)

    def valid_cred(self, username, password, pass_hash=""):
        query = Users.all().filter("username", username).get()
        if query is not None:
            pass_hash = query.password
        return username and password and auth.valid_pw(username,
                                                       password,
                                                       pass_hash)
