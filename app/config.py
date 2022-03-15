import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'\
        .format(os.environ.get('DB_USER'),
                os.environ.get('DB_PASSWORD'),
                os.environ.get('DB_HOST'),
                os.environ.get('DB_PORT'),
                os.environ.get('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
