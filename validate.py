import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


class Validate:
    def __init__(self, string):
        self.string = string

    # Username validation
    def username(self):
        return self.string and USER_RE.match(self.string)

    # Password validation
    def password(self):
        return self.string and PASS_RE.match(self.string)

    # Email validation
    def email(self):
        return not self.string or EMAIL_RE.match(self.string)
