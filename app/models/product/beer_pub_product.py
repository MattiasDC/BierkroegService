from app import db
from sqlalchemy import ForeignKey
from .product import Product
from app.models.beer_pub import BeerPub
from flask import current_app

class BeerPubProduct(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    productId = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True, nullable=False)
    beerPubId = db.Column(db.Integer, ForeignKey(BeerPub.id), primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, BeerPubProduct):
            return self.productId == other.productId and self.beerPubId == other.beerPubId
        return False

    def __hash__(self):
        return hash(repr(self))