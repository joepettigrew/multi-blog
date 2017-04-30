from handler import Handler
from models import Blogs

class NewPost(Handler):
    def get(self):
        self.user_page("blogsubmit.html", "/signup", auth_user=self.user)

    def post(self):
        # Check user's auth status
        if self.user:
            title = self.request.get("title")
            content = self.request.get("content")

            params = dict(auth_user=self.user, title=title, content=content)

            if title and content:
                # Remove <div> tag from posting
                content = content.replace("<div>", "")
                content = content.replace("</div>", "")

                # Add to Blogs entity
                blog = Blogs(title=title,
                             content=content,
                             username=self.user,
                             likes=0,
                             dislikes=0)
                blog.put()

                # Redirect to home page
                self.redirect("/welcome")
            else:
                params['error'] = "We need both the title and the blog post."
                self.render("blogsubmit.html", **params)
        else:
            self.redirect("/signup")
