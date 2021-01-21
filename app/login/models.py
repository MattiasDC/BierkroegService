from flask_login import UserMixin
from app import db
from utils.password_utils import check_password, get_hashed_password

class User(db.Model):
    username = db.Column(db.String(120), primary_key=True, nullable=False)
    _password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        ValueError("Password hash is write-only!")

    @password.setter
    def password(self, password):
        self._password = get_hashed_password(password.encode('utf8')).decode('utf8')

    def verify_password(self, password):
        return check_password(password.encode('utf8'), self._password.encode('utf8'))

class FlaskUser(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.username

    def verify_password(self, password):
        return self.user.verify_password(password)

    def is_admin(self):
        return self.user.admin

def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    return FlaskUser(user)

def create_user(username, password, admin):
    user = User(username=username, password=password, admin=admin)
    db.session.add(user)
    db.session.commit()
    return user

def get_users():
    return map(FlaskUser, User.query.all())