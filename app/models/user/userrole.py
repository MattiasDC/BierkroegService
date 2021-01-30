from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from .user import User
from .role import Role

class UserRole(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	userId = db.Column(db.String(128), ForeignKey(User.username), primary_key=True, nullable=False)
	roleId = db.Column(db.String(128), ForeignKey(Role.id), primary_key=True, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, UserRole):
			return self.userId == other.userId and self.roleId == other.roleId
		return False

	def __hash__(self):
		return hash(repr(self))

def has_role(user, role):
	return UserRole.query.filter_by(userId=user.username, roleId=role.id).one_or_none() is not None
	
def add_role(user, role):
	if not has_role(user, role):
		userRole = UserRole(userId=user.username, roleId=role.id)
		db.session.add(userRole)
		db.session.commit()

def delete_user_roles(user):
	userRoles = UserRole.query.filter_by(userId=user.username)
	db.session.delete(userRoles)
	db.session.commit()