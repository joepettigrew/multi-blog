# My files
from handlers import Handler
from handlers import MainPage
from handlers import WelcomePage
from handlers import SignUpPage
from handlers import SignIn
from handlers import SignOut
from handlers import NewPost
from handlers import EditPost
from handlers import DeletePost
from handlers import SinglePost
from handlers import LikePost
from handlers import DislikePost
from handlers import EditComment
from handlers import DeleteComment

import webapp2

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignUpPage),
    ('/welcome', WelcomePage),
    ('/([0-9]+)', SinglePost),
    ('/blogsubmit', NewPost),
    ('/edit-post', EditPost),
    ('/delete-post', DeletePost),
    ('/like-post', LikePost),
    ('/dislike-post', DislikePost),
    ('/edit-comment', EditComment),
    ('/delete-comment', DeleteComment),
    ('/login', SignIn),
    ('/logout', SignOut)
], debug=True)
