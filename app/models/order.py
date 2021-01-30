from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from app.models.beer_pub import BeerPub
from app.login.models import User

class Order(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	beerPubId = db.Column(db.Integer, ForeignKey(BeerPub.id), primary_key=True, nullable=False)
	waiter = db.Column(db.Integer, ForeignKey(User.username), primary_key=True, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, Order):
			return self.id == other.id
		return False

	def __hash__(self):
		return hash(repr(self))