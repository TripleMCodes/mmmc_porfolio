import json
import os

from flask import render_template, Blueprint
import logging
from ..models import User, ProfileImg,  MediaConfig, Client
logging.basicConfig(level=logging.DEBUG)

linktree = Blueprint(
    "linktree",
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/linktree',
    static_url_path='/linktree/static'
)

@linktree.route('/linktree')
def linktree_route():
    from ..models import LinktreeLink, LinktreeConfig
    profile_pic = ProfileImg.query.first()
    user = User.query.first()
    name = user.name.upper()
    links = LinktreeLink.query.order_by(LinktreeLink.order).all()
    config = LinktreeConfig.query.first()

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.ga4_measurement_id if ga_id else None


    media_data = {}
    try:
        entries = MediaConfig.query.all()
        
        if entries:
            for e in entries:
                if e.key in ('streaming', 'eps', 'latest'): # Added 'latest' to JSON parsing logic
                    try:
                        media_data[e.key] = json.loads(e.value) if e.value else {}
                    except Exception:
                        media_data[e.key] = {}
                else:
                    media_data[e.key] = e.value or ''
        else:
            base = os.path.join(os.path.dirname(__file__), '..')
            cfg_path = os.path.join(base, 'file.json')
            try:
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    media_data = data.get('media', {})
            except Exception:
                media_data = {}
    except Exception:
        media_data = {}


    streaming = media_data.get('streaming', {})
    
    # If no config exists, create default
    if not config:
        from ..app import db
        config = LinktreeConfig()
        db.session.add(config)
        db.session.commit()


    profile_pic_obj = ProfileImg.query.first()
    profile_picture_url = profile_pic_obj.profile_picture_url if profile_pic_obj else None
    banner_picture_url = profile_pic_obj.banner_picture_url if profile_pic_obj else None
    
    return render_template('linktree.html', links=links, config=config, name=name, profile_picture_url=profile_picture_url, banner_picture_url=banner_picture_url, streaming=streaming, ga_id=ga_id)