from flask import render_template, Blueprint, abort, request, current_app as app, jsonify
from flask_login import login_required
from app.common.loginutils import admin_required
from app.models.user.user import User
from app.models.user.role import Role
import http
from distutils.util import strtobool
from app import db
from ..blueprint import usermanagement_blueprint

@usermanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
    nonAdminRoles = list(filter(lambda role: role != Role.get_admin(), Role.get_all()))
    columns = ["Naam"] + list(map(lambda role: role.translate().capitalize(), nonAdminRoles)) + ["Acties"]

    users = list(filter(lambda user: not user.is_admin(), User.get_all()))
    rolesPerUser = {user: list(map(lambda r: r in user.get_roles(), nonAdminRoles)) for user in users}
    return render_template('usermanagement.html',
                            title="User Management",
                            columns=columns,
                            users=users,
                            rolesPerUser=rolesPerUser,
                            roles=list(map(lambda role: role.id, nonAdminRoles)))


@usermanagement_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    name = request.form['name']
    user = User.create(name, app.config['USER_PWD'])
    db.session.commit()
    return jsonify(user.id)

@usermanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    user = User.get(request.form['id'])
    user.delete()
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@usermanagement_blueprint.route('/setrole', methods=['POST'])
@login_required
@admin_required
def set_role():
    user = User.get(request.form['id'])
    role = Role.get(request.form['role'])
    enableDisable = strtobool(request.form['enable'])
    if enableDisable:
        user.add_role(role)
    else:
        user.remove_role(role)
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)