from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from app.models.order import Order
from app.models.product import Product

class OrderProduct(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	orderId = db.Column(db.Integer, ForeignKey(Order.id), primary_key=True, nullable=False)
	prudctId = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, OrderProduct):
			return self.orderId == other.orderId and self.productId == other.productId
		return False

	def __hash__(self):
		return hash(repr(self))