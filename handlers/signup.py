from handlers import Handler
from handlers import Validate
from models import Users
import auth

class SignUpPage(Handler):
    def get(self):
        self.anom_page("signup.html", "/welcome")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username, email=email)

        if not Validate(username).username():
            params['error_username'] = "Invalid username"
            have_error = True
        elif username == Users.by_username(username):
            params['error_username'] = "Same username already exists"
            have_error = True

        if not Validate(password).password():
            params['error_password'] = "Invalid password"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords didn't match"
            have_error = True

        if not Validate(email).email():
            params['error_email'] = "Invalid email address"
            have_error = True
        elif email and email == Users.by_email(email):
            params['error_email'] = "This email address is already used"
            have_error = True

        if have_error:
            self.render("signup.html", **params)
        else:
            # Create password hash
            pass_hash = auth.make_pw_hash(username, password)

            # Create user in DB
            user = Users(username=username, password=pass_hash, email=email)
            user.put()

            # Create cookie
            self.set_secure_cookie("username", username)

            # Redirect user to welcome page
            self.redirect("/welcome")
