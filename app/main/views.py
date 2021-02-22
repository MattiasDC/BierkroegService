from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models.user.role import Role

main_blueprint = Blueprint('main',
                            __name__,
                            template_folder="templates",
                            static_folder="static")

@main_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('main.html',
    	admin=Role.get_admin(),
    	waiter=Role.get_waiter(),
    	cash_desk=Role.get_cash_desk(),
    	roles=current_user.user.get_roles())