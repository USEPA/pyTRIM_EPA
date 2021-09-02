from flask import Flask
from flask_admin import Admin
from flask_assets import Environment
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from Scripts.custom.flask_api import FlaskApi
from Scripts.trim_db import Model as ModelClass
from .config import init_config
from .utils.admin_views import init_admin_views
from .utils.auth import init_auth
from .utils.hotfix import patch_flask
from .utils.routes import init_routes

# Create module instances
admin = Admin(template_mode='bootstrap3')
api = FlaskApi()
assets = Environment()
bcrypt = Bcrypt()
db = SQLAlchemy(model_class=ModelClass)
mail = Mail()
security = Security()


def create_app(testing=False):
    # Create app and load configuration
    app = Flask(__name__)
    app.logger.info("Initializing a new TRIM.Builder-WebApp")
    init_config(app, testing=False)

    # Initialize db module
    db.init_app(app)

    # Initialize email module
    mail.init_app(app)

    # Initialize user authentication module(s)
    init_auth(app, db, bcrypt, security)

    # Initialize api module
    api.init_app(app)

    # Initialize js/css compiler module
    assets.init_app(app)

    # Initialize routing module(s)
    init_routes(app)
    init_admin_views(app, admin)

    # Patch known issues with flask core
    patch_flask(app)

    # Add global template functions & vars
    app.jinja_env.filters['dir'] = dir

    @app.context_processor
    def inject_template_globals():
        return dict(site_name="TRIM.Builder")

    @app.before_first_request
    def init_app():
        if testing:
            return

        from .utils.auth import define_superusers
        app.logger.info("Initializing default superusers")
        define_superusers(app, security)

        from .utils.assets import register_assets
        app.logger.info("Building static assets")
        register_assets(assets)

    return app
