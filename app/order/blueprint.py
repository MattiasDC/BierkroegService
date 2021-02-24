from flask import Blueprint

order_blueprint = Blueprint('order', __name__,
                             url_prefix='/order',
                             template_folder='renders/templates',
                             static_folder='renders/static')

from .renders import views
from . import apiviews