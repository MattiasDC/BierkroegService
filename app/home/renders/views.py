from flask import render_template
from flask_login import login_required, current_user
from app.models.user.role import Role
from ..blueprint import home_blueprint

@home_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')