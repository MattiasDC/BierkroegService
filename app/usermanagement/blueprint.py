from flask import Blueprint

usermanagement_blueprint = Blueprint('usermanagement', __name__,
                                       url_prefix='/usermanagement',
                                       template_folder='renders/templates',
                                       static_folder='renders/static')

from .renders import views
from . import apiviews