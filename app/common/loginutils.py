from functools import wraps
from flask import current_app as app
from flask_login import current_user as user
from app.models.user.role import Role

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not user.is_authenticated:
            return app.login_manager.unauthorized()
        elif not user.is_admin():
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

def roles_required(*role_names):
    def wrapper(func):
        @wraps(func)    # Tells debuggers that is is a function wrapper
        def decorated_view(*args, **kwargs):
            if not user.is_authenticated:
                return app.login_manager.unauthorized()
            elif not user.user.has_roles(list(map(Role.get, role_names))) and not user.is_admin():
                return app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view
        
    return wrapper

def any_role_required(*role_names):
    def wrapper(func):
        @wraps(func)    # Tells debuggers that is is a function wrapper
        def decorated_view(*args, **kwargs):
            if not user.is_authenticated:
                return app.login_manager.unauthorized()
            elif not user.user.any_role(list(map(Role.get, role_names))) and not user.is_admin():
                return app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view
        
    return wrapper