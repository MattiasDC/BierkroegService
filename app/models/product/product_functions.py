from app import db
from .beer_pub_product_functions import get_beer_pub_products
from .product import Product

def get_product(id):
	return Product.query.filter_by(id=id).one_or_none()

def get_products():
	return Product.query.all()

def has_product_with_name(name, product):
	productsWithName = Product.query.filter_by(name=name)
	return productsWithName.count() > 0 and productsWithName.first() != product 

def create_product(name):
    product = Product(name=name)
    db.session.add(product)
    db.session.commit()
    return product

def delete_product(product):
	if product is None:
		return
	assert(can_delete_product(product))
	db.session.delete(product)
	db.session.commit()

def can_delete_product(product):
	return len(get_beer_pub_products(product)) == 0