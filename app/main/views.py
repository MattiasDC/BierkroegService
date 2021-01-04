from flask import render_template, Blueprint, make_response

main_blueprint = Blueprint('main',
							__name__,
							template_folder="templates",
							static_folder="static")

@main_blueprint.route('/', methods=['GET'])
def index():
    return make_response(render_template('main.html'))