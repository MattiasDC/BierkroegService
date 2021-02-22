from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from datetime import datetime

class OrderEvent(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}
    schema = current_app.config['DB_SCHEMA']

    order_id = db.Column(db.Integer, ForeignKey(f'{schema}.order.id'), primary_key=True, nullable=False)
    event_id = db.Column(db.String(128), ForeignKey(f'{schema}.event.id'), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, OrderEvent):
            return self.order_id == other.order_id and self.event_id == other.event_id
        return False

    def __hash__(self):
        return hash(repr(self))

    def delete(self):
        db.session.delete(self)

    @classmethod
    def create(cls, order, event):
        orderEvent = OrderEvent(order_id=order.id, event_id=event.id, timestamp=datetime.now())
        db.session.add(orderEvent)
        return orderEvent

    @classmethod
    def get(cls, order):
        return OrderEvent.query.filter_by(order_id=order.id)