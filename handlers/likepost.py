from handler import Handler
from models import Sentiment, Blogs
from util import post_exists


class LikePost(Handler):
    """Likes post for auth users"""
    def get(self):
        blog_id = int(self.request.get("bid"))

        # Check user's auth status
        if self.user and post_exists(blog_id):
            # Check to see if the post's owner's the same as auth user.
            if not Blogs.verify_owner(blog_id, self.user):
                # Check to see if the user has interacted with this post before
                sentiment = Sentiment.by_owner(self.user, blog_id)
                if sentiment is None:
                    sentiment = Sentiment(username=self.user,
                                          blog_id=blog_id,
                                          sentiment=True)
                    sentiment.put()

                    # Update the Datastore
                    blog = Blogs.by_id(blog_id)
                    blog.likes += 1
                    blog.put()

        self.redirect("/post/%s" % blog_id)
