from flask import Blueprint, render_template
from ..models import Blog, User, Client
import markdown
import logging

logging.basicConfig(level=logging.DEBUG)

blog = Blueprint(
    'blog_post',
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/blog-post",
    static_url_path="/blog_post/static"
)

@blog.route('/blog/<int:blog_id>')
def blog_post( blog_id):

    # print(f"The id is: {blog_id}")
    blog_post = Blog.query.filter(Blog.id == blog_id).first_or_404()

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None

    user = User.query.first()

    name = user.name.upper()
    html_content = markdown.markdown(blog_post.content)

    return render_template(
        'blog-post.html',
        blog=blog_post,
        html_content=html_content,
        name=name,
        ga_id=ga_id
    )
