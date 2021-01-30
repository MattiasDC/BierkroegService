from flask import render_template, Blueprint, abort, request, current_app as app, jsonify
from flask_login import login_required
from app.login.utils import admin_required
from app.models.user.user_functions import get_users, get_user, create_user, delete_user, has_user_with_name, is_admin
import http

usermanagement_blueprint = Blueprint('usermanagement', __name__,
					      			 url_prefix='/usermanagement',
                          			 template_folder="templates",
                          			 static_folder="static")

@usermanagement_blueprint.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

@usermanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
	return render_template('usermanagement.html',
							title="User Management",
							columns=["Naam", "Acties"],
							users=filter(lambda user: not is_admin(user), get_users()))


@usermanagement_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
	name = request.form['name']
	if has_user_with_name(name):
		abort(400, "A user with the same name already exists")
	user = create_user(name, app.config['USER_PWD'])
	return jsonify(user.username)

@usermanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
	user = get_user(request.form['name'])
	delete_user(user)
	return ("", http.HTTPStatus.NO_CONTENT)