from handlers import Handler
from models import Blogs
from util import post_exists_wrap


class EditPost(Handler):
    @post_exists_wrap
    def get(self, blog_id):
        params = dict(auth_user=self.user)

        # Verifies user's auth status and ownership of the post
        if self.user and Blogs.verify_owner(blog_id, self.user):
            blog = Blogs.by_id(blog_id)
            params['blog_id'] = blog_id
            params['title'] = blog.title
            params['content'] = blog.content
            self.user_page("editpost.html", "/signup", **params)
        else:
            self.redirect("/welcome")

    @post_exists_wrap
    def post(self, blog_id):
        title = self.request.get("title")
        content = self.request.get("content")
        blog_id = self.request.get("bid")

        # Verifies user's auth status and ownership of the post
        if self.user and Blogs.verify_owner(blog_id, self.user):
            if title and content:
                # Remove <div> tag from posting
                content = content.replace("<div>", "")
                content = content.replace("</div>", "")

                # Update the Datastore
                blog = Blogs.by_id(blog_id)
                blog.title = title
                blog.content = content
                blog.put()

                # Redirect to welcome page
                self.redirect("/welcome")
            else:
                params = dict(auth_user=self.user)
                params['title'] = title
                params['content'] = content
                params['blog_id'] = blog_id
                params['error'] = "We need both the title and the blog post."
                self.render("editpost.html", **params)
        else:
            self.redirect("/signup")
