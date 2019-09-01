from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from image_library.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from image_library.users.routes import users
    from image_library.photos.routes import photos
    from image_library.main.routes import main
    from image_library.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(photos)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
