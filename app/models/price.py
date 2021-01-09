from app import db
from sqlalchemy import ForeignKey
from app.models.product import Product
from app.models.beer_pub import BeerPub

class Price(db.Model):
	productId = db.Column(db.Integer, ForeignKey(Product.id), primary_key=True, nullable=False)
	beerPubId = db.Column(db.Integer, ForeignKey(BeerPub.id), primary_key=True, nullable=False)
	price = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f'<Price {self.price}, {self.product}>'

def get_price(productId, yearId):
	return Price.query.filter_by(productId=productId, beerPubId=beerPubId).one_or_none()