from app import db
from utils.password_utils import check_password, get_hashed_password
from sqlalchemy import ForeignKey
from flask import current_app

class User(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    username = db.Column(db.String(128), primary_key=True, nullable=False)
    _password = db.Column(db.String, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, User):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(repr(self))

    @property
    def password(self):
        ValueError("Password hash is write-only!")

    @password.setter
    def password(self, password):
        self._password = get_hashed_password(password.encode('utf8')).decode('utf8')

    def verify_password(self, password):
        return check_password(password.encode('utf8'), self._password.encode('utf8'))