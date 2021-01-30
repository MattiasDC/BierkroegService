from flask_login import LoginManager
from flask import current_app as app
from flask import redirect, url_for
from .flaskuser import FlaskUser
from app.models.user import User
from app.models.user_functions import get_user, create_user, is_admin
from app.models.role import get_admin_role
from app.models.userrole import add_role

login = LoginManager()
login.login_view = 'login.login'

def create_admin():
	admin_username = app.config["ADMIN_USERNAME"]
	admin = User.query.filter_by(username=admin_username).one_or_none()
	if not admin:
		admin = create_user(admin_username, app.config["ADMIN_PWD"])
	if not is_admin(admin):
		add_role(admin, get_admin_role())


@login.user_loader
def load_user(username):
    return FlaskUser(get_user(username))

@login.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for(login.login_view))