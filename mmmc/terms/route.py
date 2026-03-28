from flask import render_template, Blueprint
import logging
from ..models import User, Client

logging.basicConfig(level=logging.DEBUG)

terms = Blueprint(
    "terms",
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/terms",
    static_url_path="/terms/static"
)

@terms.route('/terms')
def terms_route():
    ga_id = Client.query.filter_by(name='vickykae').first()
    ga_id = ga_id.value if ga_id else None
    # Refactor: Filter by the current tenant (artist_id)
    user = User.query.first()
    
    name = user.name.upper()
    
    return render_template('terms.html', name=name, ga_id=ga_id)
