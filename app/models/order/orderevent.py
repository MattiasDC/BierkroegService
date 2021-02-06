from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from .order import Order
from .event import Event
from datetime import datetime

class OrderEvent(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	orderId = db.Column(db.Integer, ForeignKey(Order.id), primary_key=True, nullable=False)
	eventId = db.Column(db.String(128), ForeignKey(Event.id), primary_key=True, nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(other, OrderEvent):
			return self.orderId == other.orderId and self.eventId == other.eventId
		return False

	def __hash__(self):
		return hash(repr(self))

def create_order_event(order, event):
	orderEvent = OrderEvent(orderId=order.id, eventId=event.id, timestamp=datetime.now())
	db.session.add(orderEvent)
	db.session.commit()
	return orderEvent