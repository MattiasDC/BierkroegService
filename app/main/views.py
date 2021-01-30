from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models.user.userrole import get_roles

main_blueprint = Blueprint('main',
							__name__,
							template_folder="templates",
							static_folder="static")

@main_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('main.html', roles=list(map(lambda userRole: userRole.roleId, get_roles(current_user.user))))