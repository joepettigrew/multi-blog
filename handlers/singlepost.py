from handlers import Handler
from models import Users, Blogs, Sentiment, Comments
from util import post_exists_wrap


class SinglePost(Handler):
    """Renders single post as well as handling comment posting"""
    @post_exists_wrap
    def get(self, blog_id):
        blog = Blogs.by_id(blog_id)
        sentiment = Sentiment.by_owner(self.user, blog_id)
        comments = Comments.by_blog_id(blog_id)

        params = dict(blog=blog,
                      sentiment=sentiment,
                      comments=comments,
                      auth_user=self.user)

        if not blog:
            self.error(404)
            return

        self.render("singlepost.html", **params)

    @post_exists_wrap
    def post(self, blog_id):
        blog_id = int(self.request.get("bid"))
        if self.user:
            comment = self.request.get("comment")
            blog = Blogs.by_id(blog_id)
            comments = Comments.by_blog_id(blog_id)
            sentiment = Sentiment.by_owner(self.user, blog_id)

            params = dict(blog_id=blog_id,
                          auth_user=self.user,
                          blog=blog,
                          comments=comments,
                          sentiment=sentiment)

            if not comment:
                params['error_comment'] = "You didn't write any comment!"
                self.render("singlepost.html", **params)
            else:
                comment = Comments(blog_id=blog_id,
                                   comment=comment,
                                   username=self.user)
                comment.put()
                self.redirect("/post/%s#Comments" % blog_id)
        else:
            self.redirect("/post/%s#Comments" % blog_id)
