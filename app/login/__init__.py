from flask_login import LoginManager
from flask import current_app as app
from flask import redirect, url_for
import os
from .models import get_user, User
from app import db

login = LoginManager()
login.login_view = 'login.login'

def create_admin():
	admin_email = app.config["ADMIN_EMAIL"]
	if not User.query.filter_by(email=admin_email).count():
		admin = User(email=admin_email, password=app.config["DB_PWD"])
		db.session.add(admin)
		db.session.commit()

@login.user_loader
def load_user(email):
    return get_user(email)

@login.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for(login.login_view))