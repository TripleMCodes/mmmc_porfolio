from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..models import Service, FAQ, User, Client  # Corrected FAQ spelling
import logging

logging.basicConfig(level=logging.DEBUG)

service = Blueprint(
    'service',
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/service",
    static_url_path='/service/static'
)

@service.route('/service')
def service_route():
    user = User.query.first()
    name = user.name.upper() if user else "ARTIST"
    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.ga4_measurement_id

    services = Service.query.all()

    faq = FAQ.query.all()

    return render_template(
        'services.html', 
        services=services, 
        faq=faq, 
        name=name,
        ga_id=ga_id
    )