from flask import render_template, Blueprint, abort, request, current_app as app, jsonify
from flask_login import login_required
from app.login.utils import admin_required
from app.models.user.user_functions import get_users, get_user, create_user, delete_user, has_user_with_name, is_admin
from app.models.user.role import get_roles, get_admin_role, get_role, translate
from app.models.user.userrole import has_role, add_role, remove_role
import http
from distutils.util import strtobool

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
	nonAdminRoles = list(filter(lambda role: role != get_admin_role(), get_roles()))
	
	columns = ["Naam"] +\
	 list(map(lambda role: translate(role.id).capitalize(), nonAdminRoles)) +\
	  ["Acties"]

	users = list(filter(lambda user: not is_admin(user), get_users()))
	return render_template('usermanagement.html',
							title="User Management",
							columns=columns,
							users=users,
							roles={user:list(map(lambda role: [role.id, has_role(user, role)], nonAdminRoles))\
									for user in users})


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

@usermanagement_blueprint.route('/setrole', methods=['POST'])
@login_required
@admin_required
def set_role():
	user = get_user(request.form['name'])
	role = get_role(request.form['role'])
	enableDisable = strtobool(request.form['enable'])
	print(enableDisable, flush=True)
	if enableDisable:
		add_role(user, role)
	else:
		print(enableDisable, flush=True)
		remove_role(user, role)
	return ("", http.HTTPStatus.NO_CONTENT)