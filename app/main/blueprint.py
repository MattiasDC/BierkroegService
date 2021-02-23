from flask import Blueprint

main_blueprint = Blueprint('main',
                            __name__,
                            template_folder="renders/templates",
                            static_folder="renders/static")

from .renders import views