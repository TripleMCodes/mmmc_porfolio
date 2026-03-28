import pytest


@pytest.fixture
def client(monkeypatch):
    import app as app_module

    # Force in-memory sqlite for tests
    def _fake_config(a):
        a.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    monkeypatch.setattr(app_module, "_configure_database", _fake_config)

    flask_app = app_module.create_app()
    flask_app.config["TESTING"] = True

    with flask_app.app_context():
        # Create tables and seed minimal data
        app_module.db.create_all()
        from werkzeug.security import generate_password_hash
        from models import Admin, User

        admin = Admin(
            email="admin@example.com",
            password=generate_password_hash("change-me-now"),
            totp_enabled=False,
        )
        user = User(name="Artist Name", short_about="Edit this")
        app_module.db.session.add_all([admin, user])
        app_module.db.session.commit()

    with flask_app.test_client() as client:
        yield client
