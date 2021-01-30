from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models.user.userrole import has_role
from app.models.user.role import get_waiter_role

main_blueprint = Blueprint('main',
							__name__,
							template_folder="templates",
							static_folder="static")

@main_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('main.html',
    	admin=current_user.is_admin(),
    	waiter=has_role(current_user.user, get_waiter_role()))