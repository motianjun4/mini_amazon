from sqlite3 import register_adapter
from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB
from libs.my_minio import minio_client

login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    found = minio_client.bucket_exists("products")
    if not found:
        minio_client.make_bucket("products")
    else:
        print("Bucket 'products' already exists")

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    return app
