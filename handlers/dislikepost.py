from handler import Handler
from models import Sentiment
from models import Blogs

class DislikePost(Handler):
    def get(self):
        blog_id = int(self.request.get("bid"))

        # Check to see if the user has interacted with this post before.
        sentiment = Sentiment.by_owner(self.user, blog_id)
        if sentiment is None:
            sentiment = Sentiment(username=self.user,
                                  blog_id=blog_id,
                                  sentiment=False)
            sentiment.put()

            # Update the Datastore
            blog = Blogs.by_id(blog_id)
            blog.dislikes += 1
            blog.put()

        self.redirect("/post/%s" % blog_id)
