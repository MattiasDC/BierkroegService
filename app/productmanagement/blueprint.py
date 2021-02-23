from flask import Blueprint

productmanagement_blueprint = Blueprint('productmanagement', __name__,
                                        url_prefix='/productmanagement',
                                        template_folder='renders/templates',
                                        static_folder='renders/static')

from .renders import views