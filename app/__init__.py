from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB
import logging


login = LoginManager()
login.login_view = 'users.login'

class ImgFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "GET /img/" not in record.getMessage()

log = logging.getLogger("werkzeug")
log.addFilter(ImgFilter())

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)


    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    from .misc import bp as misc_bp
    app.register_blueprint(misc_bp)

    return app
