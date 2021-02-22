from app import db
from flask import current_app
from datetime import date
from utils.date_utils import overlaps
from .product.beer_pub_product import BeerPubProduct
from .product.product import Product

class BeerPub(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

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

    def add_product(self, product, price):
        BeerPubProduct.create(self, product, price)

    def remove_product(self, product):
        BeerPubProduct.get(self, product).delete()

    def get_products(self):
        return list(map(lambda bpp: Product.get(bpp.product_id), BeerPubProduct.get_all(self)))

    def get_price(self, product):
        return BeerPubProduct.get(self, product).price

    def change_price(self, product, price):
        BeerPubProduct.get(self, product).price = price
        db.session.commit()

    def get_orders(self):
        from .order.order import Order
        return list(Order.get_orders(self))

    def overlaps_with_any(self, start_date, end_date):
        return any(map(lambda bp: overlaps(self.start_date, self.end_date, bp.start_date, bp.end_date) and\
            bp != self, BeerPub.query.all()))
    
    def delete(self):
        for bpp in BeerPubProduct.get_all(self):
            bpp.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id):
        return BeerPub.query.filter_by(id=id).one_or_none()

    @classmethod
    def get_all(cls):
        return BeerPub.query.all()

    @classmethod
    def get_from_date(cls, date):
        return BeerPub.query.filter(BeerPub.start_date <= date,
                                    date <= BeerPub.end_date).one_or_none()

    @classmethod
    def get_from_product(cls, product):
        return list(map(lambda bpp: get(bpp.beer_pub_id), BeerPubProduct.query.filter_by(product_id=product.id)))
    
    @classmethod
    def create(cls, start_date, end_date):
        beer_pub = BeerPub(start_date=start_date, end_date=end_date)
        if beer_pub.overlaps_with_any(start_date, end_date):
            return None
        db.session.add(beer_pub)
        db.session.commit()
        return beer_pub
    
    @classmethod
    def get_active(cls):
        return cls.get_from_date(date.today()) 