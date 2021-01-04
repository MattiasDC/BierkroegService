from get_docker_secret import get_docker_secret
import os
from .db import create_mysql_odbc_connection

class BaseConfig(object):
    """Base configuration."""
    WTF_CSRF_ENABLED = True
    SECRET_KEY = get_docker_secret('flask_secret_key')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    SQLALCHEMY_DATABASE_URI = create_mysql_odbc_connection(os.environ['db_driver'],
    	os.environ['db_server'],
    	os.environ['db_database'],
    	os.environ['db_username'],
    	get_docker_secret('db_pwd'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_SCHEMA = os.environ['db_schema']
    
class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True