from flask import render_template, Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)
from ..models import User, Admin, Client

privacy = Blueprint(
    'privacy',
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/privacy',
    static_url_path='/privacy/static'
)

@privacy.route('/privacy')
def privacy_route():

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None
    user = User.query.first()
    name = user.name.upper() if user else "ARTIST"

    admin = Admin.query.first()
    email = admin.email if admin else "contact@example.com"

    return render_template('privacy.html', name=name, email=email, ga_id=ga_id)