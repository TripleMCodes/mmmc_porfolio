import logging
import os
from pathlib import Path
from typing import Optional

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from seed import seed_all

# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# Extensions
# ------------------------------------------------------------
db = SQLAlchemy()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _normalize_database_url(url: Optional[str]) -> Optional[str]:
    """
    Some providers still provide postgres:// URLs.
    SQLAlchemy expects postgresql://.
    """
    if not url:
        return None
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _build_sqlite_uri(sqlite_path: Optional[str]) -> str:
    """
    Builds a SQLite SQLAlchemy URI safely for:
      - relative paths (sqlite:///portfolio.db)
      - absolute Linux paths (sqlite:////var/data/portfolio.db)

    If SQLITE_PATH is not set, defaults to 'portfolio.db' in the working dir.
    """
    raw = (sqlite_path or "portfolio.db").strip()
    p = Path(raw).expanduser()

    # Absolute path -> 4 slashes
    if p.is_absolute():
        return f"sqlite:////{p.as_posix().lstrip('/')}"
    # Relative path -> 3 slashes
    return f"sqlite:///{p.as_posix()}"


def _configure_database(app: Flask) -> None:
    """
    Configure SQLALCHEMY_DATABASE_URI.

    Priority:
      1) DATABASE_URL (Postgres / Supabase / Render Postgres)
      2) SQLITE_PATH (SQLite file path, useful with persistent disk)
      3) local sqlite file: portfolio.db
    """
    database_url = _normalize_database_url(os.getenv("DATABASE_URL"))
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        print("The database is:")
        print(database_url)
        return

    # BASE_DIR = Path(__file__).resolve().parent
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'portfolio.db'}"
   
    
 
def _init_auth(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.login_view = os.getenv("LOGIN_VIEW_ENDPOINT", "admin.admin_login")
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        from .models import User  # local import avoids circular deps
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None


def _register_blueprints(app: Flask) -> None:
    from .home.route import home
    from .terms.route import terms
    from .blog_post.route import blog
    from .blog.route import all_blogs
    from .contact.route import contct
    from .privacy.route import privacy
    from .services.route import service
    from .linktree.route import linktree
    from .events.route import events
    from .media.route import media
    from .gallery.route import gallery
    from .about.route import about
    from .conditions.route import conditions
    from .admin_login.route import admin
    from .portfolio.route import portfolio

    blueprints = [
        home,
        blog,
        terms,
        contct,
        privacy,
        all_blogs,
        service,
        portfolio,
        linktree,
        events,
        media,
        gallery,
        about,
        conditions,
        admin,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)





# ------------------------------------------------------------
# App Factory
# ------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)

    # Core config
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Database config (NO SCHEMAS)
    _configure_database(app)

    # Init extensions
    db.init_app(app)
    Migrate(app, db)

    from .seed import seed_all 
    with app.app_context():
        seed_all(db)
    # Auth
    _init_auth(app)

    # Health endpoint (Render-friendly)
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    # Blueprints
    _register_blueprints(app)

    return app


# ------------------------------------------------------------
# Gunicorn entrypoints:
# 1) If you set: app = create_app() below -> gunicorn app:app
# 2) Or without it -> gunicorn "app:create_app()"
# ------------------------------------------------------------
# app = create_app()