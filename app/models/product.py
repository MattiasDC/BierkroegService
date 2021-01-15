from app import db
from flask import current_app

class Product(db.Model):
	__table_args__ = {"schema": current_app.config['DB_SCHEMA']}

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return f'<Product {self.name}>'

def get_product(id):
	return Product.query.filter_by(id=id).one_or_none()

def get_products():
	return Product.query.all()

def create_product(name):
    product = Product(name=name)
    db.session.add(product)
    db.session.commit()
    return product

def delete_product(id):
    product = get_product(id)
    db.session.delete(product)
    db.session.commit()