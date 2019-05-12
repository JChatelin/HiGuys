from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail
from config import Config


bootstrap = Bootstrap()
login = LoginManager()
login.login_view = "auth.login"
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.core import bp as core_bp
    app.register_blueprint(core_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app


from app import models
