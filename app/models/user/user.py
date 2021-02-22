from app import db
from utils.password_utils import check_password, get_hashed_password
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import current_app
from .userrole import UserRole
from .role import Role

class User(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)
    user_roles = relationship("UserRole")

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
    
    def is_admin(self):
        return UserRole.has_role(self, Role.get_admin())

    def add_role(self, role):
        UserRole.add_role(self, role)

    def remove_role(self, role):
        UserRole.get(self, role).delete()

    def get_roles(self):
        return list(map(lambda ur: Role.get(ur.role_id), self.user_roles))

    def has_roles(self, roles):
        return len(set(roles) - set(self.get_roles())) == 0

    def can_change_name(self, name):
        users_with_name = User.query.filter_by(username=name).count()
        return users_with_name <= 1 and users_with_name.one_or_none() != self
    
    def delete(self):
        for role in self.get_roles():
            self.remove_role(role)
        db.session.delete(self)

    @classmethod
    def get(cls, id):
        return User.query.filter_by(id=id).one_or_none()

    @classmethod
    def get_all(cls):
        return User.query.all()
    
    @classmethod
    def create(cls, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        return user