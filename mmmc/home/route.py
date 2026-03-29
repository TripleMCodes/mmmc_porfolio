import json
from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..models import Albums, ProfileImg, Singles, User, Skills, MediaConfig
from ..models import Blog, AboutSection, Client
import logging

logging.basicConfig(level=logging.DEBUG)

home = Blueprint(
    'home',
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/home",
    static_url_path='/home/static'
)

@home.route('/')
@home.route('/Home')
def index():
    from ..app import db
    
    media_data = {}
    entries = MediaConfig.query.all()
    for e in entries:
        if e.key in ('streaming', 'eps', 'latest'):
            try:
                media_data[e.key] = json.loads(e.value) if e.value else {}
            except Exception:
                media_data[e.key] = {}
        else:
            media_data[e.key] = e.value or ''

    
    user = User.query.first()
    name = user.name.upper() or ""
    about = user.short_about if user else ""

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.ga4_measurement_id if ga_id else None

    profile_pic_obj = ProfileImg.query.first()
    profile_picture_url = profile_pic_obj.profile_picture_url if profile_pic_obj else None
    banner_picture_url = profile_pic_obj.banner_picture_url if profile_pic_obj else None

    
    skills_query = db.session.query(Skills.skill).all()
    skills = [s[0] for s in skills_query]
    
    blogs = Blog.query.order_by(Blog.date.desc()).limit(3).all()
    if not blogs:
        blogs = []

    sections = AboutSection.query.order_by(AboutSection.order).all()
    section_data = {}
    for section in sections:
        section_data[section.section_name] = {
            'title': section.title,
            'content': json.loads(section.content) if section.content else None
        }

    eps = media_data.get('eps', [])
    featured_playlist = media_data.get('featured_playlist', '')
    singles = Singles.query.all()
    albums = Albums.query.all() 
    print(f"profile pic: {profile_picture_url}")

    return render_template(
        'index.html', 
        profile_picture_url=profile_picture_url, 
        banner_picture_url=banner_picture_url, 
        name=name, 
        short_about=about, 
        skills=skills, 
        blogs=blogs, 
        eps=eps, 
        featured_playlist=featured_playlist, 
        albums=albums, 
        singles=singles, 
        sections=section_data,
        ga_id=ga_id
    )