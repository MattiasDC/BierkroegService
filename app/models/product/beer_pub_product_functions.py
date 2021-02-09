from app import db
from typing import overload
from .beer_pub_product import BeerPubProduct
from app.models.beer_pub import BeerPub
from .product import Product

@overload
def get_beer_pub_products(beerPub : BeerPub): ...

@overload
def get_beer_pub_products(product : Product): ...

def get_beer_pub_products(arg):
    if arg is None:
        return []
    elif isinstance(arg, BeerPub):
        return BeerPubProduct.query.filter_by(beerPubId=arg.id).all()
    else:    
        return BeerPubProduct.query.filter_by(productId=arg.id).all()

def get_beer_pub_product(beerPub, product):
    return BeerPubProduct.query.filter_by(beerPubId=beerPub.id, productId=product.id).one_or_none()

def create_beer_pub_product(beerPub, product, price):
    beerPubProduct = BeerPubProduct(beerPubId=beerPub.id, productId=product.id, price=price)
    db.session.add(beerPubProduct)
    db.session.commit()
    return beerPubProduct

def delete_beer_pub_product(beerPubProduct):
    if beerPubProduct is None:
        return
    db.session.delete(beerPubProduct)
    db.session.commit()

def delete_beer_pub_products(beerPub):
    if beerPub is None:
        return
    for beerPubProduct in get_beer_pub_products(beerPub):
        delete_beer_pub_product(beerPubProduct)