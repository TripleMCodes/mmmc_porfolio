from flask import render_template, Blueprint, redirect
from ..models import User
import logging
from ..models import AboutSection, Expertise, Testimonials, HeroAbout, FoundationAbout, Journey,Client
import json

logging.basicConfig(level=logging.DEBUG)

about = Blueprint(
    'about',
    __name__,
    template_folder="./../templates",
    static_folder='./../templates/about',
    static_url_path='/about/static'
)

@about.route('/about')
def about_route():
    user = User.query.first()
    
    name = user.name.title() if user else "Artist"

    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.ga4_measurement_id if ga_id else None
    
    sections = AboutSection.query.order_by(AboutSection.order).all()
    
    section_data = {}
    for section in sections:
        section_data[section.section_name] = {
            'title': section.title,
            'content': json.loads(section.content) if section.content else None
        }
        # logging.debug(section_data)


    hero = HeroAbout.query.order_by(HeroAbout.id.asc()).first()
    foundation = FoundationAbout.query.all()
    expertise = Expertise.query.all()
    testimonials = Testimonials.query.all()
    journey_items = Journey.query.order_by(Journey.year.asc()).all()

    return render_template('about.html', sections=section_data, name=name, expertise=expertise, testimonials=testimonials, hero=hero, foundation=foundation, journey_items=journey_items, ga_id=ga_id)