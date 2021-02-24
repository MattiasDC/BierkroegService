from app import db
from flask import current_app
from sqlalchemy.orm import relationship
from datetime import date
from utils.date_utils import overlaps
from .product.beer_pub_product import BeerPubProduct
from .product.product import Product
from utils.first import first

class BeerPub(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    orders = relationship("Order")
    beer_pub_products = relationship("BeerPubProduct", cascade="all, delete-orphan")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, BeerPub):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(repr(self))

    def is_active(self):
        today = date.today()
        return self.start_date < today and today < self.end_date

    def has_product(self, product):
        return __get_beer_pub_product(product) is not None
        
    def add_product(self, product, price):
        BeerPubProduct.create(self, product, price)

    def __get_beer_pub_product(self, product):
        return first(self.beer_pub_products, lambda bpp: bpp.product_id==product.id)

    def remove_product(self, product):
        self.__get_beer_pub_product(product).delete()

    def get_products(self):
        return list(map(lambda bpp: Product.get(bpp.product_id), self.beer_pub_products))

    def get_price(self, product):
        return BeerPubProduct.get(self, product).price

    def change_price(self, product, price):
        self.__get_beer_pub_product(product).price = price

    def overlaps_with_any(self):
        return any(map(lambda bp: overlaps(self.start_date, self.end_date, bp.start_date, bp.end_date) and\
            bp != self, BeerPub.query.all()))
    
    def delete(self):
        for bpp in self.beer_pub_products:
            bpp.delete()
        db.session.delete(self)

    @classmethod
    def get(cls, id):
        return BeerPub.query.filter_by(id=id).one_or_none()

    @classmethod
    def get_all(cls):
        return BeerPub.query.all()

    @classmethod
    def __get_from_date(cls, date):
        return list(BeerPub.query.filter(BeerPub.start_date <= date, date <= BeerPub.end_date))

    @classmethod
    def get_from_product(cls, product):
        return list(map(lambda bpp: cls.get(bpp.beer_pub_id), BeerPubProduct.query.filter_by(product_id=product.id)))
    
    @classmethod
    def create(cls, start_date, end_date):
        beer_pub = BeerPub(start_date=start_date, end_date=end_date)
        if beer_pub.overlaps_with_any():
            return None
        db.session.add(beer_pub)
        return beer_pub
    
    @classmethod
    def get_active(cls):
        beer_pubs = cls.__get_from_date(date.today())
        if len(beer_pubs) == 0:
            return None
        if len(beer_pubs) == 1:
            return beer_pubs[0]
        return sorted(beer_pubs, key=lambda bp: (bp.start_date, bp.end_date))[0]