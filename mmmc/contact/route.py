from flask import render_template, request, redirect, url_for, flash, Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)
from ..models import Message, User, Admin, Client
from ..app import db

contct = Blueprint(
    "contact",
    __name__,
    template_folder="./../templates",
    static_folder="./../templates/contact",
    static_url_path="/contact/static"
)

@contct.route('/contact', methods=['GET', 'POST'])
def contact_route():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        nda_requested = 'nda' in request.form

        if not all([name, email, message]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'success': False, 'message': 'All fields are required'}, 400
            flash('All fields are required', 'error')
            return redirect(url_for('contact.contact_route'))

        new_message = Message(
            name=name,
            email=email,
            message=message,
            nda_requested=nda_requested
        )
        db.session.add(new_message)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': True, 'message': 'Message sent successfully! I\'ll respond within 48 hours.'}, 200

        flash('Message sent successfully! I\'ll respond within 48 hours.', 'success')
        return redirect(url_for('contact.contact_route'))
    
    admin = Admin.query.first()
    email = admin.email if admin else None
    user = User.query.first()
    name = user.name.upper() if user else ''
    ga_id = Client.query.filter_by(name='mmmc').first()
    ga_id = ga_id.value if ga_id else None
    return render_template('contact.html', name=name, email=email, ga_id=ga_id)