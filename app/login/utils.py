from functools import wraps
from flask import current_app as app
from flask_login import current_user as user

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not user.is_authenticated:
            return app.login_manager.unauthorized()
        elif not user.is_admin():
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view