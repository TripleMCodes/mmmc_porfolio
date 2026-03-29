from flask import render_template, Blueprint, request
import logging
from ..models import Blog, User, Client

logging.basicConfig(level=logging.DEBUG)

all_blogs = Blueprint(
    "all_blogs",
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/blogs",
    static_url_path="/all_blogs/static"
)

@all_blogs.route('/blog')
def index():
    # URL params: /blog?page=2&per_page=9
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=2, type=int)

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.ga4_measurement_id if ga_id else None

    # guardrails (so someone can't request per_page=5000)
    per_page = max(1, min(per_page, 2))
    page = max(1, page)

    pagination = (
        Blog.query
        .order_by(Blog.date.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    blogs = pagination.items
    

    user = User.query.first()
    name = user.name.upper() if user else "ARTIST"

    return render_template(
        "blog.html",
        blogs=blogs,
        pagination=pagination,
        per_page=per_page,
        name=name,
        ga_id=ga_id
    )
