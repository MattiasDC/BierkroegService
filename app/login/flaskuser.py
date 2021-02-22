from flask_login import UserMixin
from app.models.user.user import User

class FlaskUser(UserMixin):
    def __init__(self, user):
        assert(user is not None)
        self.user = user

    def get_id(self):
        return self.user.id

    def verify_password(self, password):
        return self.user.verify_password(password)

    def is_admin(self):
        return self.user is not None and self.user.is_admin()