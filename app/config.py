from get_docker_secret import get_docker_secret
import os

class BaseConfig(object):
    """Base configuration."""
    WTF_CSRF_ENABLED = True
    SECRET_KEY = get_docker_secret('flask_secret_key')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    SQLALCHEMY_DATABASE_URI = get_docker_secret('db_url')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True