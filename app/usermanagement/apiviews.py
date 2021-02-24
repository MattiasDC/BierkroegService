from flask import Blueprint, abort, request, current_app as app, jsonify
from flask_login import login_required
from app.common.loginutils import admin_required
from app.models.user.user import User
from app.models.user.role import Role
import http
from distutils.util import strtobool
from app import db
from .blueprint import usermanagement_blueprint

@usermanagement_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    name = request.form['name']
    if User.exist(name):
        abort(400, "A user with the same name already exists")
    user = User.create(name, app.config['USER_PWD'])
    db.session.commit()
    return jsonify(user.id)

@usermanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    user = User.get(request.form['id'])
    if user is not None:
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
    if user is None:
        abort(400, "An invalid user was given!")
    if role is None:
        abort(400, "An invalid role was given!")

    if enableDisable:
        user.add_role(role)
    else:
        user.remove_role(role)
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)