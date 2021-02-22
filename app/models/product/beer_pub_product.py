from app import db
from sqlalchemy import ForeignKey
from flask import current_app

class BeerPubProduct(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}
    schema = current_app.config['DB_SCHEMA']

    product_id = db.Column(db.Integer, ForeignKey(f'{schema}.product.id'), primary_key=True, nullable=False)
    beer_pub_id = db.Column(db.Integer, ForeignKey(f'{schema}.beer_pub.id'), primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, BeerPubProduct):
            return self.product_id == other.product_id and self.beer_pub_id == other.beer_pub_id
        return False

    def __hash__(self):
        return hash(repr(self))
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls, beer_pub):
        return BeerPubProduct.query.filter_by(beer_pub_id=beer_pub.id)

    @classmethod
    def get(cls, beer_pub, product):
        return BeerPubProduct.query.filter_by(beer_pub_id=beer_pub.id, product_id=product.id).one_or_none()
    
    @classmethod
    def create(cls, beer_pub, product, price):
        beerPubProduct = BeerPubProduct(beer_pub_id=beer_pub.id, product_id=product.id, price=price)
        db.session.add(beerPubProduct)
        db.session.commit()
        return beerPubProduct
    
    @classmethod
    def delete_all(cls, beer_pub):
        if beer_pub is None:
            return
        for beer_pub_product in BeerPubProduct.query.filter_by(beer_pub_id=beer_pub.id):
            beer_pub_product.delete()