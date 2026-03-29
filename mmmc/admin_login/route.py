import qrcode
import base64
from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from ..database.login import AdminLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from ..models import Admin, User, Skills, Blog, ProfileImg, Service, FAQ, Message, Gallery, AboutSection, MediaConfig, Event, LinktreeLink, LinktreeConfig, Singles, Albums, Expertise, HeroAbout, Testimonials, FoundationAbout, Journey, Client, Portfolio
from werkzeug.utils import secure_filename
import cloudinary.uploader
import os
from datetime import datetime
import logging
admin_details = AdminLogin()
import pyotp
import json, os
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)
from .config import init_cloudinary

init_cloudinary()

admin = Blueprint(
    "admin",
    __name__,
    template_folder="html",
    static_folder="scripts",
    static_url_path="/admin/static" 
)


@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get('email')
    password = request.form.get('password')

    print(email)
    print(password)
    admin_user = Admin.query.filter_by(email=email).first()
    print(admin_user)

    if not admin_user:
       
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin.admin_login'))

    if not check_password_hash(admin_user.password, password):
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin.admin_login'))

    # -------------------------------------------------
    # PASSWORD IS CORRECT → CHECK IF TOTP ENABLED
    # -------------------------------------------------
    print(f"What is totp: {admin_user.totp_enabled}")
    
    if admin_user.totp_enabled:
        session['pending_admin_id'] = admin_user.uid
        return redirect(url_for('admin.verify_totp'))

    # else:
    #     return redirect(url_for('admin.totp_setup'))

    # If no TOTP enabled → login immediately
    print("You're logged in...")
    login_user(admin_user)
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/login/totp', methods=['GET', 'POST'])
def verify_totp():
    if request.method == "GET":
        return render_template("enter_totp.html")

    code = request.form.get('code')

    pending_id = session.get('pending_admin_id')
    if not pending_id:
        flash("Session expired. Try logging in again.", "error")
        return redirect(url_for('admin.admin_login'))

    admin_user = Admin.query.get(pending_id)

    totp = pyotp.TOTP(admin_user.totp_secret)

    if totp.verify(code, valid_window=1):
        # Success
        login_user(admin_user)
        session.pop('pending_admin_id')
        return redirect(url_for('admin.admin_dashboard'))
    else:
        flash("Invalid or expired code", "error")
        return redirect(url_for('admin.verify_totp'))

@admin.route('/totp/setup')
def totp_setup():
    admin_user = Admin.query.first()  
    # If already enabled, skip
    if admin_user.totp_enabled:
        flash("TOTP already enabled.", "info")
        return redirect(url_for('admin.admin_dashboard'))

    secret = pyotp.random_base32()
    session['pending_totp_secret'] = secret

    totp = pyotp.TOTP(secret)

    uri = totp.provisioning_uri(
        name=admin_user.email,
        issuer_name="MyPortfolioCMS"
    )

    # Create QR code
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template("totp_setup.html", qr=qr_base64, secret=secret)

@admin.route('/totp/confirm', methods=['POST'])
def totp_confirm():
    code = request.form.get('code')
    secret = session.get('pending_totp_secret')

    from ..app import db

    if not secret:
        flash("Setup session expired. Try again.", "error")
        return redirect(url_for('admin.totp_setup'))

    totp = pyotp.TOTP(secret)

    if totp.verify(code):
        admin_user = Admin.query.first()
        admin_user.totp_secret = secret
        admin_user.totp_enabled = True
        db.session.commit()

        session.pop('pending_totp_secret')

        flash("TOTP enabled successfully!", "success")
        return redirect(url_for('admin.admin_dashboard'))

    flash("Invalid code. Try again.", "error")
    return redirect(url_for('admin.totp_setup'))

@admin.route('/admin dashboard')
@login_required
def admin_dashboard():
    from ..app import db
    skills = Skills.query.all()
    logging.debug([s.skill for s in skills])
    return render_template("admin_dashboard.html", skills=skills)

@admin.route('/save-update-ga4', methods=['POST'])
@login_required
def save_update_ga4():
    from ..app import db
    
    data = request.get_json() or request.form

    name = (data.get("name") or "").strip()
    ga4_measurement_id = (data.get("ga4_measurement_id") or "").strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400

    if not ga4_measurement_id:
        return jsonify({
            "success": False,
            "message": "GA4 Measurement ID is required."
        }), 400

    if not ga4_measurement_id.startswith("G-"):
        return jsonify({
            "success": False,
            "message": "Invalid GA4 Measurement ID. It should start with 'G-'."
        }), 400

    try:
        client = Client.query.filter_by(name=name).first()

        if client:
            client.ga4_measurement_id = ga4_measurement_id
            message = "GA4 Measurement ID updated successfully."
        else:
            client = Client(
                name=name,
                ga4_measurement_id=ga4_measurement_id
            )
            db.session.add(client)
            message = "GA4 Measurement ID saved successfully."

        db.session.commit()

        return jsonify({
            "success": True,
            "message": message,
            "client": {
                "id": client.id,
                "name": client.name,
                "ga4_measurement_id": client.ga4_measurement_id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An error occurred while saving GA4 data.",
            "error": str(e)
        }), 500

@admin.route('/update name', methods=['POST'])
@login_required
def upadte_name():
    from ..app import db
    # from flask import g
    data = request.get_json()
    # Only update current artist's user record
    user = User.query.first()
    if user:
        user.name = data['updated name']
        db.session.commit()
        logging.debug("Name has been updated")
        return {"message": "Name updated"}, 201
    else:
        return {"message": "User not found"}, 404

@admin.route('/update password', methods=['POST'])
@login_required
def update_password():
    from flask_login import current_user
    data = request.get_json()
    from ..app import db
    logging.debug(data)
    
    # admin_user = current_user
    admin_user = Admin.query.first()
    
    # if not admin_user.artist_id:
    #     return {"message": "Error - Admin not properly configured"}, 400
    
    if not check_password_hash(admin_user.password, data.get("old_password")):
        return {"message": "Error - passwords don't match"}, 401

    password = generate_password_hash(data.get("new_password"))
    admin_user.password = password
    db.session.commit()

    return {"message": "password updated"}, 200


@admin.route('/update email', methods=['POST'])
@login_required
def update_email():
    from flask_login import current_user
    from ..app import db
    data = request.get_json()
    logging.debug(data)
    # admin_user = current_user
    admin_user = Admin.query.first()

    
    if not check_password_hash(admin_user.password, data.get("password")):
        return {"message": "Error - please enter correct password."}, 401
    
    # Check if new email already exists
    existing = Admin.query.filter_by(email=data.get('new_email')).first()
    if existing and existing.uid != admin_user.uid:
        return {"message": "Email already in use"}, 409
    
    admin_user.email = data.get('new_email')
    db.session.commit()
    return {'message': 'Email updated'}, 200

@admin.route('/update about', methods=['POST'])
@login_required
def update_user_about():
    from ..app import db
    # from flask import g
    data = request.get_json()
    # Only update current artist's user record
    user = User.query.first()
    if user:
        user.short_about = data.get('updated about')
        db.session.commit()
        return {"message": "About has been updated"}, 200
    return {"message": "User not found"}, 404
    
@admin.route('/add skill', methods=['POST'])
@login_required
def add_new_skill():
    from ..app import db
    # from flask import g
    data = request.get_json()
   
    skill = Skills(
        skill=data.get('new skill')
    )
    db.session.add(skill)
    db.session.commit()
    logging.debug(data)
    return {"message": "skill added", "skill": {"id": skill.id, "skill": skill.skill}}, 201

@admin.route('/delete skill/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    from ..app import db
    # from flask import g
    
    skill = Skills.query.filter_by(
        id=skill_id
    ).first_or_404()
    db.session.delete(skill)
    db.session.commit()
    return {"message": "Skill deleted"}, 200

@admin.route('/update profile picture', methods=['POST'])
@login_required
def update_profile_picture():
    from ..app import db

    if 'profile_picture' not in request.files:
        return {"message": "No file part"}, 400

    file = request.files['profile_picture']

    if file.filename == '':
        return {"message": "No selected file"}, 400

    if file and allowed_file(file.filename):

        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder="profile_pictures_mmmc"
            )
        except Exception as e:
            return {"message": f"Upload failed: {str(e)}"}, 500

        image_url = upload_result.get("secure_url")
        public_id = upload_result.get("public_id")

        user = ProfileImg.query.first()

        if user:
            old_public_id = user.profile_picture  # store public_id now

            user.profile_picture = public_id
            user.profile_picture_url = image_url
              # <-- ADD THIS COLUMN
            if old_public_id:
                try:
                    cloudinary.uploader.destroy(old_public_id)
                except Exception as e:
                    print(f"Warning: Failed to delete old image: {e}")

            db.session.commit()

            return {"message": "Profile picture updated", "url": image_url}, 200

        else:
            user = ProfileImg(
                id=1,
                profile_picture=public_id,
                profile_picture_url=image_url
            )
            db.session.add(user)
            db.session.commit()

            return {"message": "Profile picture updated", "url": image_url}, 200

    return {"message": "Invalid file type"}, 400

@admin.route('/update banner picture', methods=['POST'])
@login_required
def update_banner_picture():
    from ..app import db

    if 'banner_picture' not in request.files:
        return {"message": "No file part"}, 400
    
    file = request.files['banner_picture']

    if file.filename == '':
        return {"message": "No selected file"}, 400
    
    if file and allowed_file(file.filename):
        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder="profile_pictures_mmmc"
            )
        except Exception as e:
            return {"message": f"Upload failed: {str(e)}"}, 500

        image_url = upload_result.get("secure_url")
        public_id = upload_result.get("public_id")

        user = ProfileImg.query.first()

        if user:
            old_public_id = user.banner_img  # store public_id now

            user.banner_img = public_id
            user.banner_picture_url = image_url

            if old_public_id:
                try:
                    cloudinary.uploader.destroy(old_public_id)
                except Exception as e:
                    print(f"Warning: Failed to delete old image: {e}")

            db.session.commit()

            return {"message": "Banner picture updated", "url": image_url}, 200

        else:
            user = ProfileImg(
                id=1,
                banner_img=public_id,
                banner_picture_url=image_url
            )
            db.session.add(user)
            db.session.commit()

            return {"message": "Banner picture updated", "url": image_url}, 200

    return {"message": "Invalid file type"}, 400
        

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/manage blogs')
@login_required
def manage_blogs():
    from ..app import db

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=2, type=int)

    per_page = max(1, min(per_page, 2))
    page = max(1, page)

    pagination = (
        Blog.query
        .order_by(Blog.date.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    
    blogs = pagination.items
    return render_template("manage_blogs.html", blogs=blogs, pagination=pagination)

@admin.route('/create blog', methods=['POST'])
@login_required
def create_blog():
    from ..app import db
    # from flask import g
    data = request.get_json()
    title = data.get('title')
    excerpt = data.get('excerpt')
    content = data.get('content')
    if not title or not excerpt or not content:
        return {"message": "All fields required"}, 400
    # MULTI-TENANT SAFE: Always set artist_id from context
    new_blog = Blog(
        title=title,
        excerpt=excerpt,
        content=content
    )
    db.session.add(new_blog)
    db.session.commit()
    return {"message": "Blog created"}, 201

@admin.route('/edit blog/<int:blog_id>', methods=['POST'])
@login_required
def edit_blog(blog_id):
    from ..app import db
    # from flask import g
    blog = Blog.query.filter_by(
        id=blog_id
    ).first_or_404()
    data = request.get_json()
    blog.title = data.get('title', blog.title)
    blog.excerpt = data.get('excerpt', blog.excerpt)
    blog.content = data.get('content', blog.content)
    db.session.commit()
    return {"message": "Blog updated"}, 200

@admin.route('/delete blog/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    from ..app import db
    # from flask import g
   
    blog = Blog.query.filter_by(
        id=blog_id
    ).first_or_404()
    db.session.delete(blog)
    db.session.commit()
    return {"message": "Blog deleted"}, 200
#==============================================================Services================================================
#======================================================================================================================
@admin.route('/manage services')
@login_required
def manage_services():
    from ..app import db
    # from flask import g
    services = Service.query.all()
    faq = FAQ.query.all()
    return render_template("manage_services.html", services=services, faq=faq)

@admin.route('/create service', methods=['POST'])
@login_required
def create_service():
    from ..app import db
    # from flask import g
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    icon = data.get('icon')
    price_monthly = data.get('price_monthly')
    price_yearly = data.get('price_yearly')
    if not title or not description:
        return {"message": "Title and description required"}, 400
    
    new_service = Service(
        title=title,
        description=description,
        icon=icon,
        price_monthly=price_monthly,
        price_yearly=price_yearly
    )
    db.session.add(new_service)
    db.session.commit()
    return {"message": "Service created", "service": {"id": new_service.id, "title": new_service.title, "description": new_service.description, "icon": new_service.icon, "price_monthly": new_service.price_monthly, "price_yearly": new_service.price_yearly}}, 201

@admin.route('/edit service/<int:service_id>', methods=['POST'])
@login_required
def edit_service(service_id):
    from ..app import db
    # from flask import g
   
    service = Service.query.filter_by(
        id=service_id
    ).first_or_404()
    data = request.get_json()
    service.title = data.get('title', service.title)
    service.description = data.get('description', service.description)
    service.icon = data.get('icon', service.icon)
    service.price_monthly = data.get('price_monthly', service.price_monthly)
    service.price_yearly = data.get('price_yearly', service.price_yearly)
    db.session.commit()
    return {"message": "Service updated"}, 200

@admin.route('/delete service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    from ..app import db
    # from flask import g

    service = Service.query.filter_by(
        id=service_id
    ).first_or_404()
    db.session.delete(service)
    db.session.commit()
    return {"message": "Service deleted"}, 200

@admin.route('/create faq', methods=['POST'])
@login_required
def create_faq():
    from ..app import db
    # from flask import g 

    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question:
        return {'message': 'Error - No question provided'}, 400
    if not answer:
        return {'message': 'Error - No answer provided'}, 400

    # MULTI-TENANT SAFE: Always set artist_id from context
    faq = FAQ(
        question=question,
        answer=answer
    )
    db.session.add(faq)
    db.session.commit()

    return {"message": "FAQ added", "faq": {"id": faq.id, "question": faq.question, "answer": faq.answer}}, 201

@admin.route('/edit faq/<int:faq_id>', methods=['POST'])
@login_required
def edit_faq(faq_id):
    from ..app import db
    # from flask import g
    
    faq = FAQ.query.filter_by(
        id=faq_id
    ).first_or_404()
    data = request.get_json()
    faq.question = data.get('question', faq.question)
    faq.answer = data.get('answer', faq.answer)
    db.session.commit()
    return {"message": "FAQ updated"}, 200

@admin.route('/delete faq/<int:faq_id>', methods=['POST'])
@login_required
def delete_faq(faq_id):
    from ..app import db
    # from flask import g
    
    faq = FAQ.query.filter_by(
        id=faq_id
    ).first_or_404()
    db.session.delete(faq)
    db.session.commit()
    return {"message": "FAQ deleted"}, 200

@admin.route('/manage messages')
@login_required
def manage_messages():
    from ..app import db
    # from flask import g

    messages = Message.query.order_by(Message.date.desc()).all()
    return render_template("manage_messages.html", messages=messages)

@admin.route('/mark message read/<int:message_id>', methods=['POST'])
@login_required
def mark_message_read(message_id):
    from ..app import db
    # from flask import g
    
    message = Message.query.filter_by(
        id=message_id
    ).first_or_404()
    message.read = True
    db.session.commit()
    return {"message": "Message marked as read"}, 200

@admin.route('/delete message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    from ..app import db
    # from flask import g

    message = Message.query.filter_by(
        id=message_id
    ).first_or_404()
    db.session.delete(message)
    db.session.commit()
    return {"message": "Message deleted"}, 200

@admin.route('/manage events')
@login_required
def manage_events():
    from ..app import db
    # from flask import g
    
    events = Event.query.order_by(Event.date).all()
    return render_template("manage_events.html", events=events)

@admin.route('/create event', methods=['POST'])
@login_required
def create_event():
    from ..app import db
    # from flask import g
    from datetime import datetime

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date_str = data.get('date')  # YYYY-MM-DD
    time_str = data.get('time')  # HH:MM
    location = data.get('location')
    image_url = data.get('image_url', '')
    
    if not title or not date_str:
        return {"message": "Title and date required"}, 400
    
    try:
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        event_time = None
        if time_str:
            event_time = datetime.strptime(time_str, '%H:%M').time()
        
        # MULTI-TENANT SAFE: Always set artist_id from context
        new_event = Event(
            title=title,
            description=description,
            date=event_date,
            time=event_time,
            location=location,
            image_url=image_url
        )
        db.session.add(new_event)
        db.session.commit()
        return {"message": "Event created", "event": {"id": new_event.id, "title": new_event.title, "date": new_event.date.isoformat()}}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error creating event: {str(e)}"}, 500

@admin.route('/edit event/<int:event_id>', methods=['POST'])
@login_required
def edit_event(event_id):
    from ..app import db
    # from flask import g
    from datetime import datetime
    
    event = Event.query.filter_by(
        id=event_id
    ).first_or_404()
    data = request.get_json()
    
    try:
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data and data['time']:
            event.time = datetime.strptime(data['time'], '%H:%M').time()
        if 'location' in data:
            event.location = data['location']
        if 'image_url' in data:
            event.image_url = data['image_url']
        
        db.session.commit()
        return {"message": "Event updated"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error updating event: {str(e)}"}, 500

@admin.route('/delete event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    from ..app import db
    # from flask import g
   
    event = Event.query.filter_by(
        id=event_id
    ).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}, 200

@admin.route('/manage gallery')
@login_required
def manage_gallery():
    images = Gallery.query.filter_by(type='image').order_by(Gallery.id).all()
    videos = Gallery.query.filter_by(type='video').order_by(Gallery.id).all()

    return render_template(
        "manage_gallery.html",
        images=images,
        videos=videos
    )


@admin.route('/manage media')
@login_required
def manage_media():
   
    from ..app import db
    
    media = {}
    # Try DB first
    try:
        entries = MediaConfig.query.all()
        if entries:
            for e in entries:
                if e.key in ('streaming', 'eps', 'latest'):
                    try:
                        media[e.key] = json.loads(e.value) if e.value else {}
                    except Exception:
                        media[e.key] = {}
                else:
                    media[e.key] = e.value or ''
        else:
            # fallback to file.json
            base = os.path.join(os.path.dirname(__file__), '..')
            cfg_path = os.path.join(base, 'file.json')
            try:
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    media = data.get('media', {})
            except Exception:
                media = {}
    except Exception:
        media = {}

    singles = Singles.query.all()
    albums = Albums.query.all()

    streaming = media.get('streaming', {})
    featured_playlist = media.get('featured_playlist', '')
    eps = media.get('eps', [])
    latest = media.get('latest', [])
    return render_template('manage_media.html', streaming=streaming, featured_playlist=featured_playlist, eps=eps, latest=latest, singles=singles, albums=albums)

def _get_media_from_db():
    from ..app import db
    import json
    media = {}
    try:
        entries = MediaConfig.query.all()
        for e in entries:
            if e.key in ('streaming', 'eps', 'latest'):
                try:
                    media[e.key] = json.loads(e.value) if e.value else {}
                except Exception:
                    media[e.key] = {}
            else:
                media[e.key] = e.value or ''
    except Exception:
        media = {}
    return media


def _save_media_to_db(media_dict):
    from ..app import db
    import json
    try:
        for k, v in media_dict.items():
            entry = MediaConfig.query.filter_by(key=k).first()
            if isinstance(v, (dict, list)):
                value = json.dumps(v, ensure_ascii=False)
            else:
                value = str(v) if v is not None else ''
            if entry:
                entry.value = value
            else:
                entry = MediaConfig(key=k, value=value)
                db.session.add(entry)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


@admin.route('/update streaming links', methods=['POST'])
@login_required
def update_streaming_links():
    data = request.get_json() or {}
    streaming = data.get('streaming', {})
    # Save to DB
    media = _get_media_from_db()
    media['streaming'] = streaming
    ok = _save_media_to_db({'streaming': streaming})
    if ok:
        return {"message": "Streaming links updated"}, 200
    return {"message": "Error saving streaming links"}, 500


@admin.route('/update featured playlist', methods=['POST'])
@login_required
def update_featured_playlist():
    data = request.get_json() or {}
    playlist = data.get('playlist', '')
    ok = _save_media_to_db({'featured_playlist': playlist})
    if ok:
        return {"message": "Featured playlist updated"}, 200
    return {"message": "Error saving playlist"}, 500


@admin.route('/add eps', methods=['POST'])
@login_required
def add_eps():
    data = request.get_json() or {}
    new_eps = data.get('eps')
    if not isinstance(new_eps, list):
        return {"message": "Invalid payload"}, 400
    media = _get_media_from_db()
    eps = media.get('eps', [])
    if not isinstance(eps, list):
        eps = []
    eps.extend(new_eps)
    ok = _save_media_to_db({'eps': eps})
    if ok:
        return {"message": "EP(s) added"}, 201
    return {"message": "Error saving EPs"}, 500


@admin.route('/update eps', methods=['POST'])
@login_required
def update_eps():
    data = request.get_json() or {}
    eps = data.get('eps')
    if not isinstance(eps, list):
        return {"message": "Invalid payload"}, 400
    ok = _save_media_to_db({'eps': eps})
    if ok:
        return {"message": "EP list updated"}, 200
    return {"message": "Error saving EPs"}, 500


@admin.route('/delete eps/<int:idx>', methods=['POST'])
@login_required
def delete_eps(idx):
    media = _get_media_from_db()
    eps = media.get('eps', [])
    if not isinstance(eps, list):
        return {"message": "Index out of range"}, 400
    if 0 <= idx < len(eps):
        eps.pop(idx)
        ok = _save_media_to_db({'eps': eps})
        if ok:
            return {"message": "EP deleted"}, 200
        return {"message": "Error deleting EP"}, 500
    return {"message": "Index out of range"}, 400

@admin.route('/add latest', methods=['POST'])
@login_required
def add_latest():
    data = request.get_json() or {}
    new_latest = data.get('latest')
    print(new_latest)
    if not isinstance(new_latest, list):
        return {"message": "Invalid payload"}, 400
    media = _get_media_from_db()
    latest = media.get('latest', {})
    if not isinstance(latest, dict):
        latest = {}
    
    latest['latest'] = new_latest
    print(latest)
    ok = _save_media_to_db(latest)
    ok = True
    if ok:
        return {"message": "Latest single URLs saved"}, 201
    return {"message": "Error saving latest"}, 500


@admin.route('/add single', methods=['POST'])
def add_single():
    from ..app import db

    data = request.get_json()

    title = data.get('title')
    artist = data.get('artist')
    album = data.get('album')
    links = data.get('links')
    buy_link = data.get('buy_link')

    if not all([title, artist, album, links]):
        return jsonify({'message': 'Missing fields'}), 400

    #Check if single already exists
    single = Singles.query.filter_by(
        title=title,
        artist_name=artist,
        album=album
    ).first()

    if single:
        #UPDATE
        single.links = links
        single.buy_link = buy_link
        db.session.commit()
        return jsonify({'message': 'Single updated'}), 200

    #CREATE
    new_single = Singles(
        title=title,
        artist_name=artist,
        album=album,
        links=links
    )

    db.session.add(new_single)
    db.session.commit()

    return jsonify({'message': 'Single added'}), 201


@admin.route('/add album', methods=['POST'])
def add_or_update_album():
    
    from ..app import db
    data = request.get_json()

    try:
        released_date = datetime.strptime(
            data.get('released_date'), "%Y-%m-%d"
        ).date()
    except Exception:
        return jsonify({'message': 'Invalid release date'}), 400

    title = data.get('title')
    artist = data.get('artist')
    link = data.get('link')
    buy_link = data.get('buy_link')


    if not all([title, artist, released_date, link]):
        return jsonify({'message': 'Missing fields'}), 400

    album = Albums.query.filter_by(
        title=title,
        artist_name=artist,
        released_date=released_date
    ).first()

    if album:
        #UPDATE
        album.link = link
        album.buy_link = buy_link
        db.session.commit()
        return jsonify({'message': 'Album updated'}), 200

    #CREATE
    album = Albums(
        title=title,
        artist_name=artist,
        released_date=released_date,
        link=link,
        buy_link=buy_link
    )

    db.session.add(album)
    db.session.commit()

    return jsonify({'message': 'Album created'}), 201

@admin.route('/delete album', methods=['POST'])
def delete_album():
    from ..app import db

    data = request.get_json()

    try:
        released_date = datetime.strptime(
            data.get('released_date'), "%Y-%m-%d"
        ).date()
    except Exception:
        return jsonify({'message': 'Invalid release date'}), 400

    title = data.get('title')
    artist = data.get('artist')

    if not all([title, artist, released_date]):
        return jsonify({'message': 'Missing fields'}), 400

    album = Albums.query.filter_by(
        title=title,
        artist=artist,
        released_date=released_date
    ).first()

    if not album:
        return jsonify({'message': 'Album not found'}), 404

    db.session.delete(album)
    db.session.commit()

    return jsonify({'message': 'Album deleted'}), 200

@admin.route('/delete single', methods=['POST'])
def delete_single():
    from ..app import db
    data = request.get_json()

    title = data.get('title')
    artist = data.get('artist')
    album = data.get('album')

    if not all([title, artist, album]):
        return jsonify({'message': 'Missing fields'}), 400

    single = Singles.query.filter_by(
        title=title,
        artist=artist,
        album=album
    ).first()

    if not single:
        return jsonify({'message': 'Single not found'}), 404

    db.session.delete(single)
    db.session.commit()

    return jsonify({'message': 'Single deleted'}), 200

#==========================================gallary============================================

import cloudinary.uploader

@admin.route('/upload gallery image', methods=['POST'])
@login_required
def upload_gallery_image():
    from ..app import db

    images_count = Gallery.query.filter_by(type='image').count()
    if images_count >= 5:
        return {"message": "Maximum 5 images allowed. Delete an old image first."}, 400

    if 'image' not in request.files:
        return {"message": "No file part"}, 400

    file = request.files['image']

    if file.filename == '':
        return {"message": "No selected file"}, 400

    if file and allowed_file(file.filename):

        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder="gallery_images_mmmc"
            )
        except Exception as e:
            return {"message": f"Upload failed: {str(e)}"}, 500

        image_url = upload_result.get("secure_url")
        public_id = upload_result.get("public_id")

        title = request.form.get('title', '')

        new_item = Gallery(
            type='image',
            url=public_id,
            cloud_url=image_url,
            title=title
        )

        db.session.add(new_item)
        db.session.commit()

        return {
            "message": "Image uploaded",
            "item": {
                "id": new_item.id,
                "url": new_item.cloud_url,
                "title": new_item.title
            }
        }, 201

    return {"message": "Invalid file type"}, 400


@admin.route('/delete gallery item/<int:item_id>', methods=['POST'])
@login_required
def delete_gallery_item(item_id):
    from ..app import db

    item = Gallery.query.filter_by(id=item_id).first_or_404()

    if item.type == 'image':
        if item.url:  # this is public_id now
            try:
                cloudinary.uploader.destroy(item.url)
            except Exception as e:
                print(f"Warning: Failed to delete image: {e}")

    db.session.delete(item)
    db.session.commit()

    return {"message": "Item deleted"}, 200

@admin.route('/add gallery video', methods=['POST'])
@login_required
def add_gallery_video():
    from ..app import db
    data = request.get_json()
    url = data.get('url')
    title = data.get('title', '')
    if not url:
        return {"message": "URL required"}, 400
    new_item = Gallery(
        type='video',
        url=url,
        title=title,
        cloud_url=""  # no cloud URL for videos, but keeping field for consistency

    )
    db.session.add(new_item)
    db.session.commit()
    return {"message": "Video added", "item": {"id": new_item.id, "url": new_item.url, "title": new_item.title}}, 201

#======================================about

@admin.route('/manage about')
@login_required
def manage_about():
    from ..app import db
    import json
    from types import SimpleNamespace

    raw_sections = AboutSection.query.order_by(AboutSection.order).all()

    # Build a wrapper that supports both index access (sections[0]) and
    # attribute/get access (sections.hero, sections.get('foundation')).
    class SectionsWrapper:
        def __init__(self, rows):
            self._list = []
            self._map = {}
            for r in rows:
                # parse JSON content if possible
                parsed = {}
                if r.content:
                    try:
                        parsed = json.loads(r.content)
                    except Exception:
                        parsed = r.content

                # store a mapping-friendly dict for get-style access
                self._map[r.section_name] = {"title": r.title, "content": parsed}

                # store a simple namespace for index-based access used in template
                self._list.append(SimpleNamespace(title=r.title, content=parsed))

        def __getattr__(self, name):
            if name in self._map:
                return self._map[name]
            raise AttributeError(name)

        def __getitem__(self, idx):
            return self._list[idx]

        def get(self, key, default=None):
            return self._map.get(key, default)


    foundation = FoundationAbout.query.order_by(FoundationAbout.id.asc()).first()
    hero = HeroAbout.query.order_by(HeroAbout.id.asc()).first()

    expertise = Expertise.query.all()
    testimonials = Testimonials.query.all()

    journey_items = Journey.query.order_by(Journey.year.asc()).all()

    sections = SectionsWrapper(raw_sections)
    return render_template("manage_about.html", sections=sections, expertise=expertise, testimonials=testimonials, hero=hero, foundation=foundation, journey_items=journey_items)

@admin.route('/update about section', methods=['POST'])
@login_required
def update_about_section():
    from ..app import db
    data = request.get_json()
    section_name = data.get('section_name')
    title = data.get('title')
    content = data.get('content')  # JSON string

    logging.debug(data)

    section = AboutSection.query.filter_by(
        section_name=section_name
    ).first()
    if not section:
        section = AboutSection(
            section_name=section_name
        )
        db.session.add(section)
    section.title = title
    section.content = content
    db.session.commit()
    return {"message": "About section updated"}, 200

#==============================================================Linktree===================================================
#======================================================================================================================
@admin.route('/manage linktree')
@login_required
def manage_linktree():
    from ..app import db
    
   
    links = LinktreeLink.query.order_by(LinktreeLink.order).all()
    config = LinktreeConfig.query.first()
    
    if not config:
        config = LinktreeConfig()
        db.session.add(config)
        db.session.commit()
    
    return render_template("manage_linktree.html", links=links, config=config)

@admin.route('/update linktree config', methods=['POST'])
@login_required
def update_linktree_config():
    from app import db
    data = request.get_json()

    config = LinktreeConfig.query.first()
    if not config:
       
        config = LinktreeConfig()
        db.session.add(config)
    
    if data.get('avatar'):
        config.avatar = data.get('avatar')
    if data.get('name'):
        config.name = data.get('name')
    if data.get('handle'):
        config.handle = data.get('handle')
    if data.get('bio'):
        config.bio = data.get('bio')
    if data.get('email'):
        config.email = data.get('email')
    
    db.session.commit()
    return {"message": "Configuration updated"}, 200


@admin.route("/hero", methods=["POST"])
@login_required
def upsert_hero():
    from ..app import db

    data = request.get_json() or {}
    hero_title = (data.get("hero-title") or "").strip()
    hero_brief = (data.get("hero-brief") or "").strip()

    if not hero_title:
        return {"message": "Error - Please provide hero title"}, 400
    if not hero_brief:
        return {"message": "Error - Please provide hero brief"}, 400

    hero = HeroAbout.query.order_by(HeroAbout.id.asc()).first()

    if not hero:
        hero = HeroAbout(hero_title=hero_title, hero_brief=hero_brief)
        db.session.add(hero)
        db.session.commit()
        return {
            "message": "About hero section successfully created.",
            "hero": {"id": hero.id, "hero_title": hero.hero_title, "hero_brief": hero.hero_brief}
        }, 201

    hero.hero_title = hero_title
    hero.hero_brief = hero_brief
    db.session.commit()

    return {
        "message": "About hero section successfully updated.",
        "hero": {"id": hero.id, "hero_title": hero.hero_title, "hero_brief": hero.hero_brief}
    }, 200


@admin.route("/foundation", methods=["POST"])
@login_required
def upsert_foundation():
    from ..app import db

    data = request.get_json() or {}
    paragraphs_arr = data.get("paragraphsArr") or []

    # Safely grab the two paragraphs (default to empty string)
    p1 = (paragraphs_arr[0] if len(paragraphs_arr) > 0 else "") or ""
    p2 = (paragraphs_arr[1] if len(paragraphs_arr) > 1 else "") or ""
    p1, p2 = p1.strip(), p2.strip()

    # Check if table is empty
    table_empty = db.session.query(FoundationAbout.id).first() is None

    if table_empty:
        # Insert two rows
        db.session.add_all([
            FoundationAbout(id=1, title="paragraph_one", paragraphs=p1),
            FoundationAbout(id=2, title="paragraph_two", paragraphs=p2),
        ])
        db.session.commit()
        return {"message": "Foundation section successfully created."}, 201

    # Table has data -> update existing rows; create if missing
    row1 = FoundationAbout.query.get(1)
    row2 = FoundationAbout.query.get(2)

    if row1 is None:
        row1 = FoundationAbout(id=1, title="paragraph_one", paragraphs=p1)
        db.session.add(row1)
    else:
        row1.title = "paragraph_one"
        row1.paragraphs = p1

    if row2 is None:
        row2 = FoundationAbout(id=2, title="paragraph_two", paragraphs=p2)
        db.session.add(row2)
    else:
        row2.title = "paragraph_two"
        row2.paragraphs = p2

    db.session.commit()
    return {"message": "Foundation section successfully updated."}, 200

@admin.route("/journey", methods=["POST"])
@login_required
def create_journey():
    from ..app import db

    data = request.get_json() or {}
    year = data.get("year")
    desc = (data.get("desc") or "").strip()

    try:
        year = int(year)
    except (TypeError, ValueError):
        return {"message": "Year must be an integer."}, 400

    if not desc:
        return {"message": "Description is required."}, 400

    item = Journey(year=year, desc=desc)
    db.session.add(item)
    db.session.commit()

    return {
        "message": "Journey item created.",
        "journey": {"id": item.id, "year": item.year, "desc": item.desc}
    }, 201

@admin.route("/journey/<int:item_id>", methods=["PUT"])
@login_required
def update_journey(item_id):
    from ..app import db

    item = Journey.query.get(item_id)
    if not item:
        return {"message": "Journey item not found."}, 404

    data = request.get_json() or {}
    year = data.get("year")
    desc = (data.get("desc") or "").strip()

    try:
        year = int(year)
    except (TypeError, ValueError):
        return {"message": "Year must be an integer."}, 400

    if not desc:
        return {"message": "Description is required."}, 400

    item.year = year
    item.desc = desc
    db.session.commit()

    return {
        "message": "Journey item updated.",
        "journey": {"id": item.id, "year": item.year, "desc": item.desc}
    }, 200

@admin.route("/journey/<int:item_id>", methods=["DELETE"])
@login_required
def delete_journey(item_id):
    from ..app import db

    item = Journey.query.get(item_id)
    if not item:
        return {"message": "Journey item not found."}, 404

    db.session.delete(item)
    db.session.commit()

    return {"message": "Journey item deleted.", "id": item_id}, 200

@admin.route('/add-expertise', methods=['POST'])
@login_required
def add_experitse():
    from ..app import db

    data = request.get_json()

    if not data.get('expertise'):
        return {"message": "Please provide expertise title"}, 400
    expertise = data.get('expertise')

    if not data.get('desc'):
        return {"message": "Please provide expertise description"}, 400
    desc = data.get('desc')

    if not data.get('icon'):
        return {"message": "Please provide an icon"}, 400
    icon = data.get('icon')

    new_expertise = Expertise(
        expertise=expertise,
        desc=desc,
        icon=icon
    )

    db.session.add(new_expertise)
    db.session.commit()

    return {
        "message": f"'{expertise}' added successfully.",
        "exp_id": new_expertise.exp_id,
        "expertise": new_expertise.expertise,
        "desc": new_expertise.desc,
        "icon": new_expertise.icon,
    }, 201


@admin.route('/delete-expertise/<int:exp_id>', methods=['DELETE'])
@login_required
def delete_expertise(exp_id):
    from ..app import db

    exp = Expertise.query.get(exp_id)
    if not exp:
        return {"message": "Expertise not found."}, 404

    db.session.delete(exp)
    db.session.commit()
    return {"message": "Expertise deleted successfully.", "exp_id": exp_id}, 200

@admin.route('/add-testimonial', methods=['POST'])
@login_required
def add_testimonial():
    from ..app import db

    data = request.get_json() or {}

    if not data.get('artist_name'):
        return {'message': 'Please provide artist name'}, 400
    artist_name = data.get('artist_name')

    if not data.get('testimonial'):
        return {'message': 'Please provide testimonial'}, 400
    testimonial = data.get('testimonial')

    if not data.get('artist_social_link'):
        return {"message": "Please provide artist social link"}, 400
    artist_social = data.get('artist_social_link')

    new_testimonial = Testimonials(
        artist_name=artist_name,
        testimonial=testimonial,
        artist_social=artist_social
    )

    db.session.add(new_testimonial)
    db.session.commit()

    return {
        "message": "New testimonial successfully added.",
        "t_id": new_testimonial.t_id,
        "artist_name": new_testimonial.artist_name,
        "testimonial": new_testimonial.testimonial,
        "artist_social": new_testimonial.artist_social
    }, 201

@admin.route('/delete-testimonial/<int:t_id>', methods=['DELETE'])
@login_required
def delete_testimonial(t_id):
    from ..app import db

    t = Testimonials.query.get(t_id)
    if not t:
        return {"message": "Testimonial not found."}, 404

    db.session.delete(t)
    db.session.commit()
    return {"message": "Testimonial deleted successfully.", "t_id": t_id}, 200



@admin.route('/create linktree link', methods=['POST'])
@login_required
def create_linktree_link():
    from ..app import db
    # from flask import g
    data = request.get_json()
    text = data.get('text')
    url = data.get('url')
    is_secondary = data.get('is_secondary', False)
    
    if not text or not url:
        return {"message": "Text and URL are required"}, 400
    
    # Get the next order value for current artist
    max_order = db.session.query(db.func.max(LinktreeLink.order)).scalar() or 0
    
    # MULTI-TENANT SAFE: Always set artist_id from context
    new_link = LinktreeLink(
        text=text,
        url=url,
        is_secondary=is_secondary,
        order=max_order + 1
    )
    db.session.add(new_link)
    db.session.commit()
    return {"message": "Link created successfully"}, 201

@admin.route('/edit linktree link/<int:link_id>', methods=['POST'])
@login_required
def edit_linktree_link(link_id):
    from ..app import db
    # from flask import g
    link = LinktreeLink.query.filter_by(
        id=link_id
    ).first_or_404()
    data = request.get_json()
    
    link.text = data.get('text', link.text)
    link.url = data.get('url', link.url)
    link.is_secondary = data.get('is_secondary', link.is_secondary)
    
    db.session.commit()
    return {"message": "Link updated successfully"}, 200

@admin.route('/delete linktree link/<int:link_id>', methods=['POST'])
@login_required
def delete_linktree_link(link_id):
    from ..app import db
    # from flask import g
    link = LinktreeLink.query.filter_by(
        id=link_id
    ).first_or_404()
    db.session.delete(link)
    db.session.commit()
    return {"message": "Link deleted successfully"}, 200

# ---------------------------
# Manage Portfolio Page
# ---------------------------
@admin.route("/manage-portfolio", methods=["GET"])
@login_required
def manage_portfolio():

    samples = Portfolio.query.order_by(Portfolio.id.desc()).all()

    return render_template(
        "manage_portfolio.html",
        samples=samples
    )


@admin.route("/api/portfolio", methods=["POST"])
@login_required
def add_sample():

    from ..app import db
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    project_url = data.get("project_url")

    if not title or not description:
        return jsonify({"error": "Title and description required"}), 400

    new_sample = Portfolio(
        title=title,
        description=description,
        project_url=project_url
    )

    db.session.add(new_sample)
    db.session.commit()

    return jsonify({
        "message": "Portfolio item added",
        "sample": {
            "id": new_sample.id,
            "title": new_sample.title,
            "description": new_sample.description,
            "project_url": new_sample.project_url
        }
    }), 201


@admin.route("/api/portfolio", methods=["GET"])
@login_required
def get_portfolio():

    page = request.args.get("page", 1, type=int)
    per_page = 5

    pagination = Portfolio.query.order_by(
        Portfolio.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    samples = pagination.items

    portfolio_list = []

    for sample in samples:
        portfolio_list.append({
            "id": sample.id,
            "title": sample.title,
            "description": sample.description,
            "project_url": sample.project_url
        })

    return jsonify({
        "portfolio": portfolio_list,
        "total_pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }) 

@admin.route("/api/portfolio/<int:sample_id>", methods=["DELETE"])
@login_required
def delete_sample(sample_id):
    from ..app import db
    sample = Portfolio.query.get(sample_id)

    if not sample:
        return jsonify({"error": "Sample not found"}), 404

    db.session.delete(sample)
    db.session.commit()

    return jsonify({
        "message": "Portfolio item deleted"
    }), 200

