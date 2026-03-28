from flask import render_template, Blueprint
from ..models import Gallery, User, Client
from urllib.parse import urlparse, parse_qs
from urllib.parse import urlparse, parse_qs

gallery = Blueprint(
    'gallery',
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/gallery',
    static_url_path='/gallery/static'
)



def extract_youtube_id(url):
    if not url:
        return None

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if 'v' in query:
        return query['v'][0]

    if parsed.path.startswith('/embed/'):
        return parsed.path.split('/embed/')[1].split('/')[0]

    if 'youtu.be' in parsed.netloc:
        return parsed.path[1:]

    return None

@gallery.route('/gallery')
def gallery_route():
    user = User.query.first()
    name = user.name.upper()

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None

    # gallery_items = Gallery.query.order_by(Gallery.id).all()

    # for item in gallery_items:
    #     if item.type == 'video':
    #         url = item.url
    #         if not url:
    #             item.video_id = None
    #             continue

    #         parsed = urlparse(url)
    #         query = parse_qs(parsed.query)
            
    #         if 'v' in query:
    #             item.video_id = query['v'][0]
    #         elif parsed.path.startswith('/embed/'):
    #             item.video_id = parsed.path.split('/embed/')[1].split('/')[0]
    #         elif 'youtu.be' in parsed.netloc:
    #             item.video_id = parsed.path[1:]
    #         else:
    #             item.video_id = url  # fallback
                
    # return render_template('gallery.html', gallery_items=gallery_items, name=name, ga_id=ga_id)

    gallery_items = Gallery.query.order_by(Gallery.id).all()

    images = []
    videos = []

    for item in gallery_items:
        if item.type == 'image':
            images.append(item)

        elif item.type == 'video':
            item.video_id = extract_youtube_id(item.url)
            videos.append(item)

    return render_template(
        'gallery.html',
        images=images,
        videos=videos,
        name=name,
        ga_id=ga_id
    )