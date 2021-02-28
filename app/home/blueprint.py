from flask import Blueprint

home_blueprint = Blueprint('home',
                            __name__,
							url_prefix='/home',
                            template_folder='renders/templates',
                            static_folder='renders/static')

from .renders import views