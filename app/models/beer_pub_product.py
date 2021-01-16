from app import db
from sqlalchemy import ForeignKey
from app.models.product import Product
from app.models.beer_pub import BeerPub
from flask import current_app

class BeerPubProduct(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	productId = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True, nullable=False)
	beerPubId = db.Column(db.Integer, ForeignKey(BeerPub.id), primary_key=True, nullable=False)
	price = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f'<Product {self.product}, Price: {self.price}>'

def get_beer_pub_products(beerPub):
	return BeerPubProduct.query.filter_by(beerPubId=beerPub.id).all()

def get_beer_pub_product(beerPubId, productId):
	return BeerPubProduct.query.filter_by(beerPubId=beerPubId, productId=productId).one_or_none()

def create_beer_pub_product(beerPubId, productId, price):
    beerPubProduct = BeerPubProduct(beerPubId=beerPubId, productId=productId, price=price)
    db.session.add(beerPubProduct)
    db.session.commit()
    return beerPubProduct

def delete_beer_pub_product(beerPubId, productId):
    beerPubProduct = get_beer_pub_product(beerPubId, productId)
    db.session.delete(beerPubProduct)
    db.session.commit()