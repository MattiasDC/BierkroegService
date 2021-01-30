from flask_login import UserMixin
from app.models.user import User
from app.models.userrole import has_role
from app.models.role import get_admin_role

class FlaskUser(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.username

    def verify_password(self, password):
        return self.user.verify_password(password)

    def is_admin(self):
        return has_role(self.user, get_admin_role())