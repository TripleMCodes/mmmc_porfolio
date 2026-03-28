from flask import render_template, Blueprint, abort
from ..models import User, Admin, Client
import logging

logging.basicConfig(level=logging.DEBUG)

conditions = Blueprint(
    'conditions',
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/conditions',
    static_url_path='/conditions/static'
)

@conditions.route('/conditions')
def conditions_route():
    user = User.query.first()

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None

    admin = Admin.query.first()
    name = user.name.upper()
    email = admin.email if admin else ""

    return render_template(
        'conditions.html',
        name=name,
        email=email,
        ga_id=ga_id
    )
