from .user import User
from .userrole import delete_user_roles, has_role
from .role import get_admin_role
from app import db

def get_user(username):
    return User.query.filter_by(username=username).one_or_none()

def get_users():
    return User.query.all()

def has_user_with_name(name):
    return User.query.filter_by(username=name).count() > 0

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user):
    if user is None:
        return
    delete_user_roles(user)
    db.session.delete(user)
    db.session.commit()

def is_admin(user):
    return has_role(user, get_admin_role())