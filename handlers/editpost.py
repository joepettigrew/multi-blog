from handler import Handler
from models import Blogs

class EditPost(Handler):
    def get(self):
        params = dict(auth_user=self.user)
        blog_id = self.request.get("bid")
        if Blogs.verify_owner(blog_id, self.user):
            blog = Blogs.by_id(blog_id)
            params['blog_id'] = blog_id
            params['title'] = blog.title
            params['content'] = blog.content
            self.user_page("editpost.html", "/signup", **params)
        else:
            self.redirect("/welcome")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        blog_id = self.request.get("bid")
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
