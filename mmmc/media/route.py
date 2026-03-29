from flask import Blueprint, render_template
import logging
import os, json
from ..models import MediaConfig, Singles, Albums, User, Client

media = Blueprint(
    'media',
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/media',
    static_url_path='/media/static'
)

@media.route('/media')
def media_route():

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

    # 2. Scope Discography to current artist
    singles = Singles.query.all()
    albums = Albums.query.all()

    # 3. Extract variables from the scoped media_data dictionary
    streaming = media_data.get('streaming', {})
    featured_playlist = media_data.get('featured_playlist', '')
    eps = media_data.get('eps', [])
    latest = media_data.get('latest', [])

    # 4. Scope User to current artist
    user = User.query.first()
    name = user.name.upper() if user else "ARTIST"

    return render_template(
        'media.html', 
        streaming=streaming, 
        featured_playlist=featured_playlist, 
        eps=eps, 
        latest=latest, 
        singles=singles, 
        albums=albums, 
        user=user, 
        name=name,
        ga_id=ga_id
    )