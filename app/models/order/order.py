from app import db
from sqlalchemy import ForeignKey
from flask import current_app
from app.models.beer_pub import BeerPub
from app.models.user.user import User

class Order(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    beerPubId = db.Column(db.Integer, ForeignKey(BeerPub.id), nullable=False)
    waiter = db.Column(db.String(128), ForeignKey(User.username), nullable=False)
    paidAtOrder = db.Column(db.Boolean, nullable=False)
    table = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Order):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))