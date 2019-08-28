from flask import render_template, Blueprint, make_response

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET'])
def index():
    return make_response(render_template('main/index.html'))