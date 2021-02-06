from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from .order import Order
from app.models.product.product import Product

class OrderProduct(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	orderId = db.Column(db.Integer, ForeignKey(Order.id), primary_key=True, nullable=False)
	productId = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True, nullable=False)
	amount = db.Column(db.Integer, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, OrderProduct):
			return self.orderId == other.orderId and self.productId == other.productId and self.amount == other.amount
		return False

	def __hash__(self):
		return hash(repr(self))

def create_order_products(order, products, amounts):
	assert(len(products) == len(amounts))
	orderProducts = [OrderProduct(orderId=order.id, productId=product.id, amount=amount) for product, amount in zip(products, amounts)]
	for orderProduct in orderProducts:
		db.session.add(orderProduct)
	db.session.commit()
	return orderProducts