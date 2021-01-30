from get_docker_secret import get_docker_secret
import os
from utils.db_utils import create_mysql_odbc_connection_string_url
from datetime import timedelta

class BaseConfig(object):
    """Base configuration."""
    WTF_CSRF_ENABLED = True
    SECRET_KEY = get_docker_secret('flask_secret_key')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    DB_PWD = get_docker_secret('db_pwd')
    SQLALCHEMY_DATABASE_URI = create_mysql_odbc_connection_string_url(os.environ['db_driver'],
    	os.environ['db_server'],
        os.environ['db_port'],
    	os.environ['db_database'],
    	os.environ['db_username'],
    	DB_PWD)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_SCHEMA = os.environ['db_schema']
    ADMIN_USERNAME = os.environ['admin_username']
    ADMIN_PWD = get_docker_secret('admin_pwd')
    USER_PWD = get_docker_secret('user_pwd')
    REMEMBER_COOKIE_DURATION = timedelta(days=1)
    
class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True