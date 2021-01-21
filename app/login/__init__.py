from flask_login import LoginManager
from flask import current_app as app
from flask import redirect, url_for
from .models import get_user, User, create_user
from app import db

login = LoginManager()
login.login_view = 'login.login'

def create_admin():
	admin_username = app.config["ADMIN_USERNAME"]
	if not User.query.filter_by(username=admin_username).count():
		admin = create_user(username, app.config["ADMIN_PWD"], True)
		db.session.add(admin)
		db.session.commit()

@login.user_loader
def load_user(username):
    return get_user(username)

@login.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for(login.login_view))