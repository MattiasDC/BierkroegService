from flask import Blueprint

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
                                    url_prefix='/pubmanagement',
                                    template_folder='renders/templates',
                                    static_folder='renders/static')

from .renders import views