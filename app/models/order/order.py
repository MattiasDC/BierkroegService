from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import current_app
from .orderproduct import OrderProduct
from .event import Event
from .orderevent import OrderEvent
from app.models.product.beer_pub_product import BeerPubProduct
from app.models.product.product import Product
from app.models.user.user import User
from datetime import datetime
from utils.first import first

class Order(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}
    schema = current_app.config['DB_SCHEMA']

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    beer_pub_id = db.Column(db.Integer, ForeignKey(f'{schema}.beer_pub.id'), nullable=False)
    waiter = db.Column(db.Integer, ForeignKey(f'{schema}.user.id'), nullable=False)
    paid_at_order = db.Column(db.Boolean, nullable=False)
    table = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String)
    order_events = relationship("OrderEvent", cascade="all, delete-orphan")
    order_products = relationship("OrderProduct", cascade="all, delete-orphan")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Order):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))

    def get_waiter(self):
        return User.get(self.waiter)

    def get_products(self):
        return list(map(lambda op: Product.get(op.product_id), self.order_products))

    def get_product_amount(self, product):
        return OrderProduct.get(self, product).amount

    def get_nof_units(self):
        return sum(map(get_product_amount, get_products))

    def get_product_price(self, product):
        from app.models.beer_pub import BeerPub
        beer_pub = BeerPub.get(self.beer_pub_id)
        return self.get_product_amount(product)*BeerPubProduct.get(beer_pub, product).price

    def get_total_price(self):
        return sum(map(lambda p: self.get_product_price(p), self.get_products()))

    def get_last_event(self):
        return Event.get(sorted(self.order_events, key=lambda order_event: order_event.timestamp, reverse=True)[0].event_id)
    
    def get_ordered_time(self):
        return first(self.order_events, lambda oe: oe.event_id==Event.get_ordered_id()).timestamp

    def add_event(self, event):
        OrderEvent.create(self, event)
    
    def delete(self):
        db.session.delete(self)

    def __add_order_products(self, products, amounts):
        assert(len(products) == len(amounts))
        order_products = [OrderProduct(order_id=self.id, product_id=product.id, amount=amount) for product, amount in zip(products, amounts)]
        for order_product in order_products:
            db.session.add(order_product)
    
    @classmethod
    def get(cls, order_id):
        return Order.query.filter_by(id=order_id).one_or_none()
    
    @classmethod
    def create(cls, beer_pub, waiter, products, amounts, table, paid_at_order, remarks=""):
        order = Order(beer_pub_id=beer_pub.id, waiter=waiter.id, paid_at_order=paid_at_order, table=table, remarks=remarks)
        db.session.add(order)
    
        order.add_event(Event.get_ordered())
        order.__add_order_products(products, amounts)