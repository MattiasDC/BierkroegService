from flask import Blueprint

login_blueprint = Blueprint('login',
                            __name__,
                            url_prefix='/login',
                            template_folder='renders/templates',
                            static_folder='renders/static')

from .renders import views