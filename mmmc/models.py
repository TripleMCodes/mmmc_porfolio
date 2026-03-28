from sqlite3 import Date
from .app import db
from flask_login import UserMixin
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"

    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    totp_secret = db.Column(db.String(32), nullable=True)
    totp_enabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.email}"
    
    def get_id(self):
        return str(self.uid)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
        

class User(db.Model, UserMixin):
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    short_about = db.Column(db.Text, nullable=False)

    def get_id(self):
        return str(self.uid)

class Skills(db.Model, UserMixin):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    skill = db.Column(db.Text, nullable=False)


class ProfileImg(db.Model):
    __tablename__ = 'ProfileImg'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profile_picture = db.Column(db.Text, nullable=True)
    profile_picture_url = db.Column(db.Text, nullable=True)
    banner_img = db.Column(db.Text, nullable=True)
    banner_picture_url = db.Column(db.Text, nullable=True)


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    reading_time = db.Column(db.Integer, nullable=True)

    # def __repr__(self):
    #     return f"<Blog {self.title} (artist_id={self.artist_id})>"


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=True)
    price_monthly = db.Column(db.Float, nullable=True)
    price_yearly = db.Column(db.Float, nullable=True)


class FAQ(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    nda_requested = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    read = db.Column(db.Boolean, default=False)


class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    url = db.Column(db.Text, nullable=False)        # public_id
    cloud_url = db.Column(db.Text, nullable=False)  # actual URL
    title = db.Column(db.Text, nullable=True)


class MediaConfig(db.Model):
    __tablename__ = 'media_config'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    key = db.Column(db.String(64), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=True)  # JSON string or plain text

class Singles(db.Model):
    __tablename__ = 'singles'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    artist_name = db.Column(db.String(64), nullable=False)
    album = db.Column(db.String(64), nullable=False)
    links = db.Column(db.Text, nullable=False)
    buy_link = db.Column(db.Text, nullable=True)


class Albums(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist_name = db.Column(db.String(128), nullable=False)
    released_date = db.Column(db.Date, nullable=False)
    link = db.Column(db.Text, nullable=False)
    buy_link = db.Column(db.Text, nullable=True)


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    location = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())


class AboutSection(db.Model):
    __tablename__ = 'about_section'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    section_name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # JSON string for complex data
    order = db.Column(db.Integer, nullable=False, default=0)


class HeroAbout(db.Model): 
    __tablename__ = "hero_about"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hero_title = db.Column(db.Text, nullable=False)
    hero_brief  = db.Column(db.Text, nullable=False)

class FoundationAbout(db.Model):
    __tablename__ = "foundation_about"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    paragraphs = db.Column(db.Text, nullable=False)


class Journey(db.Model):
    __tablename__ = "journey"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    
class Expertise(db.Model):
    __tablename__ = 'expertise'

    exp_id = db.Column(db.Integer, primary_key=True, nullable=False)
    expertise = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=False)

class Testimonials(db.Model):
    __tablename__ = "testimonials"

    t_id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_name = db.Column(db.Text, nullable=False)
    testimonial = db.Column(db.Text, nullable=False)
    artist_social = db.Column(db.Text, nullable=False)


class LinktreeLink(db.Model):
    __tablename__ = 'linktree_link'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)  # Button text with emoji
    url = db.Column(db.Text, nullable=False)
    is_secondary = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, nullable=False, default=0)


#for ga4 analytics
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    ga4_measurement_id = db.Column(db.String(20), nullable=True)

class LinktreeConfig(db.Model):
    __tablename__ = 'linktree_config'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    avatar = db.Column(db.Text, nullable=False, default='V')
    name = db.Column(db.Text, nullable=False, default='Vickeykae')
    handle = db.Column(db.Text, nullable=False, default='')
    bio = db.Column(db.Text, nullable=False, default='')
    email = db.Column(db.Text, nullable=False, default='example@gmail.com')


class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_url = db.Column(db.Text, nullable=True)