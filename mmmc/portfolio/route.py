from flask import render_template, request, Blueprint
from ..models import Portfolio, User, Client
import logging

logging.basicConfig(level=logging.DEBUG)

portfolio = Blueprint(
    'portfolio',
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/portfolio",
    static_url_path='/portfolio/static'
)




@portfolio.route('/portfolio')
def my_portfolio():

    user = User.query.first()

    name = user.name.upper() if user else ""
    about = user.short_about if user else ""

    page = request.args.get("page", 1, type=int)
    per_page = 6

    ga_id = Client.query.filter_by(name='mmmc').first()

    pagination = Portfolio.query.order_by(
        Portfolio.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    samples = pagination.items

    return render_template(
        'portfolio.html',
        name=name,
        about=about,
        samples=samples,
        pagination=pagination,
        ga_id=ga_id
    )