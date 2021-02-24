from flask import render_template, Blueprint, current_app as app
from flask_login import login_required
from app.common.loginutils import admin_required
from app.models.user.user import User
from app.models.user.role import Role
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