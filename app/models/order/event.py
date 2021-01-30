from app import db
from flask import current_app

class Event(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	id = db.Column(db.String(128), primary_key=True, nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, Event):
			return self.id == other.id
		return False

	def __hash__(self):
		return hash(repr(self))