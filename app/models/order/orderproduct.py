from app import db
from sqlalchemy import ForeignKey
from flask import current_app

class OrderProduct(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}
    schema = current_app.config['DB_SCHEMA']

    order_id = db.Column(db.Integer, ForeignKey(f'{schema}.order.id'), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, ForeignKey(f'{schema}.product.id'), primary_key=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, OrderProduct):
            return self.orderId == other.order_id and self.product_id == other.product_id and self.amount == other.amount
        return False

    def __hash__(self):
        return hash(repr(self))

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_all(cls, order):
        return OrderProduct.query.filter_by(order_id=order.id)

    @classmethod
    def get(cls, order, product):
        return OrderProduct.query.filter_by(order_id=order.id, product_id=product.id).one_or_none()