from flask import render_template, Blueprint
from ..models import Event, User, Client
import logging

events = Blueprint(
    'events',
    __name__,
    template_folder='./../templates',
    static_folder='./../templates/events',
    static_url_path='/events/static'
)

@events.route('/events')
def events_route():
    
    user = User.query.first()
    name = user.name.upper() if user else "ARTIST"
    events_list = Event.query.order_by(Event.date.desc()).all()
    
    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None
    
    return render_template('events.html', events=events_list, name=name, ga_id=ga_id)