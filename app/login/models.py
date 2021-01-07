from flask_login import UserMixin
from app import db
from utils.passwordutils import check_password, get_hashed_password

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True, nullable=False)
    _password = db.Column(db.String,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

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
        return self.user.email

    def verify_password(self, password):
        return self.user.verify_password(password)

def get_user(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    return FlaskUser(user)