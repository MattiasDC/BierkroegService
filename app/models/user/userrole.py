from app import db
from sqlalchemy import ForeignKey
from flask import current_app

class UserRole(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}
    schema = current_app.config['DB_SCHEMA']

    user_id = db.Column(db.Integer, ForeignKey(f'{schema}.user.id'), primary_key=True, nullable=False)
    role_id = db.Column(db.String(128), ForeignKey(f'{schema}.role.id'), primary_key=True, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, UserRole):
            return self.userId == other.userId and self.roleId == other.roleId
        return False

    def __hash__(self):
        return hash(repr(self))

    def delete(self):
        db.session.delete(self)

    @classmethod
    def get(cls, user, role):
        return UserRole.query.filter_by(user_id=user.id, role_id=role.id).one_or_none()
    
    @classmethod
    def has_role(cls, user, role):
        return cls.get(user, role) is not None
    
    @classmethod
    def has_roles(cls, user, roles):
        return all(map(lambda role: UserRole.query.filter_by(user_id=user.id, role_id=role.id).one_or_none() is not None, roles))
    
    @classmethod
    def add_role(cls, user, role):
        if not cls.has_role(user, role):
            userRole = UserRole(user_id=user.id, role_id=role.id)
            db.session.add(userRole)